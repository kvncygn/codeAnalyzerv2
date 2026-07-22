using System;
using System.Collections.Generic;

namespace Shop
{
    /// <summary>
    /// Order processing. Doc comment above should be EXCLUDED from method span.
    /// </summary>
    public class Orders
    {
        // ---- TCF methods (analyzed) ----

        public void TCF_ProcessOrder(int qty, bool rush)
        {
            var items = new List<string>();
            items.Add("widget");          // library List.Add -> NOT a helper
            var total = CalcTotal(qty);   // project method -> helper
            if (rush)                      // +1 complexity
            {
                total = ApplyRush(total); // project method -> helper
            }
            for (int i = 0; i < qty; i++) // +1 complexity
            {
                Log("line " + i);         // project method -> helper
            }
            Console.WriteLine(total);
        }

        public int TCF_Validate(int qty)
        {
            /* multi-line
               comment block
               spanning 3 lines */
            if (qty <= 0 || qty > 100)    // || adds +1, if adds +1
            {
                return -1;
            }

            return CalcTotal(qty);        // helper reuse across TCF methods
        }

        // This TCF method only calls another TCF method -> must be IGNORED (no helper edge)
        public void TCF_Bootstrap()
        {
            TCF_ProcessOrder(1, false);
        }

        // ---- non-TCF methods ----

        private int CalcTotal(int qty) => qty * 10;   // helper (called by 2 TCF methods)

        private int ApplyRush(int total) => total + 5; // helper

        private void Log(string msg) => Console.WriteLine(msg); // helper

        // Never called by any TCF method -> NOT a helper
        private void Unused()
        {
            Console.WriteLine("dead code");
        }
    }
}
