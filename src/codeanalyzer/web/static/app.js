// Local-only UI behaviour. No network calls; everything runs in the browser.
(function () {
  "use strict";

  // Outlier thresholds (used for highlighting and the "only outliers" toggle).
  var CX_WARN = 10, CX_HIGH = 20, LOW_COMMENT = 0.05, LOW_COMMENT_MIN_LINES = 20;

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function isLowComment(m) {
    return m.total >= LOW_COMMENT_MIN_LINES && m.ratio < LOW_COMMENT;
  }
  function isOutlier(m) {
    return m.cx > CX_WARN || isLowComment(m);
  }

  // --- File download helpers (all client-side; nothing leaves the machine) ------
  function downloadBlob(name, text, mime) {
    var blob = new Blob([text], { type: mime + ";charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url; a.download = name;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
  function csvCell(v) {
    v = String(v);
    return /[",\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
  }
  function downloadCsv(name, rows) {
    downloadBlob(name, rows.map(function (r) { return r.map(csvCell).join(","); }).join("\r\n"), "text/csv");
  }

  // --- Loading overlay while an analysis runs ----------------------------------
  (function () {
    var overlay = document.getElementById("loading-overlay");
    if (!overlay) return;
    // Hide overlay before the page enters BFCache, and on any restore — runs on
    // every page so a back-navigation can never leave it stuck visible.
    window.addEventListener("pagehide", function () { overlay.hidden = true; });
    window.addEventListener("pageshow", function () { overlay.hidden = true; });
    var form = document.querySelector("form[data-analyze]");
    if (!form) return;
    form.addEventListener("submit", function () {
      var folder = form.querySelector('[name="folder"]');
      if (folder && !folder.value.trim()) return; // let server show the empty-path error
      overlay.hidden = false;
    });
  })();

  // --- Expand / collapse the whole source tree ---------------------------------
  var root = document.querySelector(".tree-root");
  function setAll(open) {
    if (!root) return;
    root.querySelectorAll("details").forEach(function (d) { d.open = open; });
  }
  var expandBtn = document.getElementById("expand-all");
  var collapseBtn = document.getElementById("collapse-all");
  if (expandBtn) expandBtn.addEventListener("click", function () { setAll(true); });
  if (collapseBtn) collapseBtn.addEventListener("click", function () { setAll(false); });

  // --- Download the plain-text report ------------------------------------------
  var dlBtn = document.getElementById("download-btn");
  var reportEl = document.getElementById("report-text");
  if (dlBtn && reportEl) {
    dlBtn.addEventListener("click", function () {
      downloadBlob("code-analysis-report.txt", reportEl.value, "text/plain");
    });
  }

  // --- Download the whole result as JSON ---------------------------------------
  var jsonBtn = document.getElementById("download-json");
  var jsonEl = document.getElementById("report-json");
  if (jsonBtn && jsonEl) {
    jsonBtn.addEventListener("click", function () {
      // Re-serialize so the file is pretty-printed rather than the minified blob.
      var pretty = JSON.stringify(JSON.parse(jsonEl.textContent), null, 2);
      downloadBlob("code-analysis-report.json", pretty, "application/json");
    });
  }

  // --- Sortable tables (click a header to sort; click again to reverse) ---------
  (function () {
    document.querySelectorAll("table.sortable").forEach(function (table) {
      var headers = table.querySelectorAll("thead th");
      headers.forEach(function (th, col) {
        var mode = th.getAttribute("data-sort");
        if (!mode) return;
        th.classList.add("th-sort");
        th.addEventListener("click", function () {
          var body = table.tBodies[0];
          var rows = Array.prototype.slice.call(body.rows);
          var asc = th.getAttribute("data-dir") !== "asc";
          rows.sort(function (a, b) {
            var x = a.cells[col].textContent.trim();
            var y = b.cells[col].textContent.trim();
            var cmp = mode === "num"
              ? (parseFloat(x) || 0) - (parseFloat(y) || 0)
              : x.localeCompare(y);
            return asc ? cmp : -cmp;
          });
          headers.forEach(function (h) { h.removeAttribute("data-dir"); });
          th.setAttribute("data-dir", asc ? "asc" : "desc");
          rows.forEach(function (r) { body.appendChild(r); });
        });
      });
    });
  })();

  // --- File summary: live filter + CSV export ----------------------------------
  (function () {
    var f = document.getElementById("file-filter");
    var t = document.getElementById("file-table");
    if (t && f) {
      f.addEventListener("input", function () {
        var q = f.value.trim().toLowerCase();
        t.querySelectorAll("tbody tr").forEach(function (tr) {
          tr.style.display = tr.textContent.toLowerCase().indexOf(q) === -1 ? "none" : "";
        });
      });
    }
    var csv = document.getElementById("file-csv");
    if (t && csv) {
      csv.addEventListener("click", function () {
        var rows = [];
        t.querySelectorAll("tr").forEach(function (tr) {
          var cells = Array.prototype.map.call(tr.querySelectorAll("th,td"), function (c) {
            return c.textContent.trim();
          });
          rows.push(cells);
        });
        downloadCsv("file-summary.csv", rows);
      });
    }
  })();

  // --- Generic client-side paginator (filter + adjustable page size) -----------
  // cfg: { dataId, section, container, renderItem(item), filterFn(item)|null,
  //        sizeSelect, noResults }
  function createPaginator(cfg) {
    var dataEl = document.getElementById(cfg.dataId);
    if (!dataEl) return null;
    var data = JSON.parse(dataEl.textContent);
    var container = cfg.container;
    var pagers = Array.prototype.slice.call(cfg.section.querySelectorAll(".pager"));
    var filtered = data;
    var page = 0;
    var size = cfg.sizeSelect ? (parseInt(cfg.sizeSelect.value, 10) || 50) : 50;

    function render() {
      var pages = Math.max(1, Math.ceil(filtered.length / size));
      if (page >= pages) page = pages - 1;
      if (page < 0) page = 0;
      var start = page * size;
      var slice = filtered.slice(start, start + size);
      if (cfg.noResults) cfg.noResults.hidden = filtered.length !== 0;
      container.innerHTML = slice.map(cfg.renderItem).join("");
      var multi = filtered.length > size;
      pagers.forEach(function (p) {
        p.hidden = !multi;
        if (!multi) return;
        p.querySelector(".pager-info").textContent =
          "Page " + (page + 1) + " / " + pages + "  ·  " +
          (start + 1) + "–" + (start + slice.length) + " of " + filtered.length;
        p.querySelector(".pg-prev").disabled = page === 0;
        p.querySelector(".pg-next").disabled = page >= pages - 1;
      });
    }
    function refilter() {
      filtered = cfg.filterFn ? data.filter(cfg.filterFn) : data;
      page = 0;
      render();
    }
    if (cfg.sizeSelect) {
      cfg.sizeSelect.addEventListener("change", function () {
        size = parseInt(cfg.sizeSelect.value, 10) || 50;
        page = 0; render();
      });
    }
    pagers.forEach(function (p) {
      p.querySelector(".pg-prev").addEventListener("click", function () { page--; render(); });
      p.querySelector(".pg-next").addEventListener("click", function () { page++; render(); });
    });

    render();
    return {
      data: data,
      refilter: refilter,
      jumpTo: function (idx) {  // clear filters externally before calling, then jump
        filtered = data; page = Math.floor(idx / size); render();
      },
    };
  }

  // --- TCF Method Details ------------------------------------------------------
  function tcfCard(m) {
    var n = m.helpers.length;
    var helpers = n
      ? m.helpers.map(function (h) { return '<span class="chip">' + esc(h) + "</span>"; }).join("")
      : '<span class="muted">none — this method calls no project helpers</span>';
    var pct = m.ratio * 100;
    var cxClass = m.cx > CX_HIGH ? "cx-high" : (m.cx > CX_WARN ? "cx-warn" : "cx-ok");
    var low = isLowComment(m);
    var lowBadge = low ? '<span class="badge badge-low" title="Low comment ratio for its size">Low comments</span>' : "";
    return (
      '<details class="method' + (isOutlier(m) ? " is-outlier" : "") + '" id="' + esc(m.id) + '">' +
        "<summary>" +
          '<span class="twisty"></span><span class="ico ico-fn"></span>' +
          '<span class="method-name">' + esc(m.name) + "</span>" +
          '<span class="method-loc mono">' + esc(m.file) + ":" + m.start + "–" + m.end + "</span>" +
          '<span class="badge ' + cxClass + '" title="Cyclomatic complexity">Cyclomatic Complexity: ' + m.cx + "</span>" +
          lowBadge +
          '<span class="badge badge-help" title="Project helper functions this method calls">' +
            "calls " + n + (n === 1 ? " helper" : " helpers") + "</span>" +
        "</summary>" +
        '<div class="method-body">' +
          '<div class="metrics">' +
            "<span class='metric'><b>" + m.total + "</b> total</span>" +
            "<span class='metric'><b>" + m.code + "</b> code</span>" +
            "<span class='metric'><b>" + m.comment + "</b> comment</span>" +
            "<span class='metric'><b>" + m.inline + "</b> inline</span>" +
            "<span class='metric'><b>" + m.blank + "</b> blank</span>" +
            "<span class='metric'><b>" + pct.toFixed(0) + "%</b> comments</span>" +
          "</div>" +
          '<div class="ratio-bar' + (low ? " ratio-low" : "") + '"><span style="width:' + pct.toFixed(1) + '%"></span></div>' +
          '<div class="helpers-line"><span class="helpers-label">Helper functions this method calls:</span>' +
            helpers + "</div>" +
        "</div>" +
      "</details>"
    );
  }

  var tcfSection = document.getElementById("tcf-section");
  if (tcfSection && document.getElementById("tcf-data")) {
    var tcfSearch = document.getElementById("tcf-search");
    var tcf = createPaginator({
      dataId: "tcf-data",
      section: tcfSection,
      container: document.getElementById("tcf-list"),
      sizeSelect: document.getElementById("tcf-size"),
      noResults: document.getElementById("tcf-noresults"),
      renderItem: tcfCard,
      filterFn: function (m) {
        var q = tcfSearch ? tcfSearch.value.trim().toLowerCase() : "";
        if (!q) return true;
        return m.name.toLowerCase().indexOf(q) !== -1 || m.file.toLowerCase().indexOf(q) !== -1;
      },
    });
    if (tcf) {
      if (tcfSearch) tcfSearch.addEventListener("input", tcf.refilter);

      var csv = document.getElementById("tcf-csv");
      if (csv) {
        csv.addEventListener("click", function () {
          var rows = [["method", "file", "start", "end", "total", "code", "comment",
                       "inline", "blank", "comment_ratio", "complexity", "helpers"]];
          tcf.data.forEach(function (m) {
            rows.push([m.name, m.file, m.start, m.end, m.total, m.code, m.comment,
                       m.inline, m.blank, m.ratio, m.cx, m.helpers.join("; ")]);
          });
          downloadCsv("tcf-methods.csv", rows);
        });
      }

      var indexById = {};
      tcf.data.forEach(function (m, i) { indexById[m.id] = i; });
      document.querySelectorAll(".method-link").forEach(function (link) {
        link.addEventListener("click", function (e) {
          e.preventDefault();
          var id = link.getAttribute("href").slice(1);
          if (!(id in indexById)) return;
          if (tcfSearch) tcfSearch.value = "";
          tcf.jumpTo(indexById[id]);
          var card = document.getElementById(id);
          if (card) {
            card.open = true;
            card.scrollIntoView({ block: "center" });
            card.classList.add("flash");
            setTimeout(function () { card.classList.remove("flash"); }, 1200);
          }
        });
      });
    }
  }

  // --- Helper Usage Summary ----------------------------------------------------
  function helperRow(h) {
    var callers = h.callers.map(function (c) { return '<span class="chip">' + esc(c) + "</span>"; }).join("");
    return (
      "<tr>" +
        '<td class="l mono"><span class="chip chip-strong">' + esc(h.name) + "</span></td>" +
        '<td class="l mono muted">' + esc(h.file) + "</td>" +
        '<td class="n">' + h.callers.length + "</td>" +
        '<td class="l">' + callers + "</td>" +
      "</tr>"
    );
  }

  var helperSection = document.getElementById("helper-section");
  if (helperSection && document.getElementById("helper-data")) {
    var helperSearch = document.getElementById("helper-search");
    var helper = createPaginator({
      dataId: "helper-data",
      section: helperSection,
      container: document.getElementById("helper-list"),
      sizeSelect: document.getElementById("helper-size"),
      noResults: document.getElementById("helper-noresults"),
      renderItem: helperRow,
      filterFn: function (h) {
        var q = helperSearch ? helperSearch.value.trim().toLowerCase() : "";
        if (!q) return true;
        return h.name.toLowerCase().indexOf(q) !== -1 ||
               h.file.toLowerCase().indexOf(q) !== -1 ||
               h.callers.join(" ").toLowerCase().indexOf(q) !== -1;
      },
    });
    if (helper) {
      if (helperSearch) helperSearch.addEventListener("input", helper.refilter);
      var hcsv = document.getElementById("helper-csv");
      if (hcsv) {
        hcsv.addEventListener("click", function () {
          var rows = [["helper", "defined_in", "called_by_count", "callers"]];
          helper.data.forEach(function (h) {
            rows.push([h.name, h.file, h.callers.length, h.callers.join("; ")]);
          });
          downloadCsv("helper-usage.csv", rows);
        });
      }
    }
  }

  // --- Unused Method Summary ---------------------------------------------------
  function unusedRow(m) {
    return (
      "<tr>" +
        '<td class="l mono"><span class="chip chip-strong">' + esc(m.name) + "</span></td>" +
        '<td class="l mono muted">' + esc(m.file) + "</td>" +
        '<td class="l mono">' + m.start + "–" + m.end + "</td>" +
        '<td class="n">' + m.cx + "</td>" +
      "</tr>"
    );
  }

  var unusedSection = document.getElementById("unused-section");
  if (unusedSection && document.getElementById("unused-data")) {
    var unusedSearch = document.getElementById("unused-search");
    var unused = createPaginator({
      dataId: "unused-data",
      section: unusedSection,
      container: document.getElementById("unused-list"),
      sizeSelect: document.getElementById("unused-size"),
      noResults: document.getElementById("unused-noresults"),
      renderItem: unusedRow,
      filterFn: function (m) {
        var q = unusedSearch ? unusedSearch.value.trim().toLowerCase() : "";
        if (!q) return true;
        return m.name.toLowerCase().indexOf(q) !== -1 ||
               m.file.toLowerCase().indexOf(q) !== -1;
      },
    });
    if (unused) {
      if (unusedSearch) unusedSearch.addEventListener("input", unused.refilter);
      var ucsv = document.getElementById("unused-csv");
      if (ucsv) {
        ucsv.addEventListener("click", function () {
          var rows = [["method_name", "defined_in", "start_line", "end_line", "complexity"]];
          unused.data.forEach(function (m) {
            rows.push([m.name, m.file, m.start, m.end, m.cx]);
          });
          downloadCsv("unused-methods.csv", rows);
        });
      }
    }
  }

  // --- Unused Definitions Summary ----------------------------------------------
  function unusedDefRow(d) {
    return (
      "<tr>" +
        '<td class="l mono"><span class="chip chip-strong">' + esc(d.name) + "</span></td>" +
        '<td class="l mono">' + esc(d.type) + "</td>" +
        '<td class="l mono muted">' + esc(d.file) + "</td>" +
        '<td class="n">' + d.line + "</td>" +
      "</tr>"
    );
  }

  var unusedDefSection = document.getElementById("unused-def-section");
  if (unusedDefSection && document.getElementById("unused-def-data")) {
    var unusedDefSearch = document.getElementById("unused-def-search");
    var unusedDef = createPaginator({
      dataId: "unused-def-data",
      section: unusedDefSection,
      container: document.getElementById("unused-def-list"),
      sizeSelect: document.getElementById("unused-def-size"),
      noResults: document.getElementById("unused-def-noresults"),
      renderItem: unusedDefRow,
      filterFn: function (d) {
        var q = unusedDefSearch ? unusedDefSearch.value.trim().toLowerCase() : "";
        if (!q) return true;
        return d.name.toLowerCase().indexOf(q) !== -1 ||
               d.type.toLowerCase().indexOf(q) !== -1 ||
               d.file.toLowerCase().indexOf(q) !== -1;
      },
    });
    if (unusedDef) {
      if (unusedDefSearch) unusedDefSearch.addEventListener("input", unusedDef.refilter);
      var udcsv = document.getElementById("unused-def-csv");
      if (udcsv) {
        udcsv.addEventListener("click", function () {
          var rows = [["name", "type", "defined_in", "line"]];
          unusedDef.data.forEach(function (d) {
            rows.push([d.name, d.type, d.file, d.line]);
          });
          downloadCsv("unused-definitions.csv", rows);
        });
      }
    }
  }

  // --- Native folder picker (index page) ---------------------------------------
  // Calls the local /pick-folder endpoint, which opens an OS dialog on this machine.
  (function () {
    var btn = document.getElementById("browse-btn");
    var input = document.getElementById("folder");
    if (!btn || !input) return;
    btn.hidden = false; // reveal only when JS is available
    btn.addEventListener("click", function () {
      btn.disabled = true;
      var prev = btn.textContent;
      btn.textContent = "Opening…";
      fetch("pick-folder", { credentials: "same-origin" })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d.available === false) {
            btn.hidden = true; // no GUI here — fall back to manual entry
            return;
          }
          if (d.path) { input.value = d.path; input.focus(); }
        })
        .catch(function () { /* keep manual entry */ })
        .then(function () { btn.disabled = false; btn.textContent = prev; });
    });
  })();
})();
