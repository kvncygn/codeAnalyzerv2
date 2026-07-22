using System;
using System.Collections.Generic;

// Auto-generated TCF file #1 (TCF methods only; helpers live elsewhere).
namespace Enterprise
{
    public class Service1
    {
        // TCF entry point #0
        public int TCF_Svc1_Op0(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            for (int i = 0; i < 1; i++)
            {
                acc.Add(i * 1); // inline
            }
            for (int i = 0; i < 2; i++)
            {
                acc.Add(i * 2); // inline
            }
            if (n > 2 || n < -2)   // if + ||
            {
                acc.Add(n - 2);
            }
            acc.Add(Helpers0.H0_37(n));   // cross-file project helper
            acc.Add(Helpers0.H0_11(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #1
        public int TCF_Svc1_Op1(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            for (int i = 0; i < 1; i++)
            {
                acc.Add(i * 1); // inline
            }
            for (int i = 0; i < 2; i++)
            {
                acc.Add(i * 2); // inline
            }
            if (n > 2 || n < -2)   // if + ||
            {
                acc.Add(n - 2);
            }
            acc.Add(Helpers2.H2_41(n));   // cross-file project helper
            acc.Add(Helpers0.H0_4(n));   // cross-file project helper
            acc.Add(Helpers1.H1_18(n));   // cross-file project helper
            acc.Add(TCF_Svc1_Op0(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #2
        /* multi-line note
           describing the routine */
        public int TCF_Svc1_Op2(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            for (int i = 0; i < 1; i++)
            {
                acc.Add(i * 1); // inline
            }
            if (n > 1 || n < -1)   // if + ||
            {
                acc.Add(n - 1);
            }
            acc.Add(Helpers0.H0_12(n));   // cross-file project helper
            acc.Add(Helpers0.H0_4(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #3
        public int TCF_Svc1_Op3(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            if (n > 0 || n < -0)   // if + ||
            {
                acc.Add(n - 0);
            }
            if (n > 1 || n < -1)   // if + ||
            {
                acc.Add(n - 1);
            }
            if (n > 2 || n < -2)   // if + ||
            {
                acc.Add(n - 2);
            }
            acc.Add(Helpers0.H0_23(n));   // cross-file project helper
            acc.Add(Helpers2.H2_46(n));   // cross-file project helper
            acc.Add(Helpers0.H0_16(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #4
        public int TCF_Svc1_Op4(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            acc.Add(Helpers1.H1_20(n));   // cross-file project helper
            acc.Add(Helpers1.H1_12(n));   // cross-file project helper
            acc.Add(TCF_Svc1_Op3(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #5
        public int TCF_Svc1_Op5(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            if (n > 0 || n < -0)   // if + ||
            {
                acc.Add(n - 0);
            }
            if (n > 1 || n < -1)   // if + ||
            {
                acc.Add(n - 1);
            }
            if (n > 2 || n < -2)   // if + ||
            {
                acc.Add(n - 2);
            }
            acc.Add(Helpers1.H1_33(n));   // cross-file project helper
            acc.Add(Helpers0.H0_11(n));   // cross-file project helper
            acc.Add(Helpers1.H1_10(n));   // cross-file project helper
            acc.Add(TCF_Svc1_Op4(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #6
        /* multi-line note
           describing the routine */
        public int TCF_Svc1_Op6(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            for (int i = 0; i < 1; i++)
            {
                acc.Add(i * 1); // inline
            }
            for (int i = 0; i < 2; i++)
            {
                acc.Add(i * 2); // inline
            }
            acc.Add(Helpers0.H0_34(n));   // cross-file project helper
            acc.Add(Helpers0.H0_3(n));   // cross-file project helper
            acc.Add(Helpers2.H2_35(n));   // cross-file project helper
            acc.Add(TCF_Svc1_Op5(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #7
        /* multi-line note
           describing the routine */
        public int TCF_Svc1_Op7(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            acc.Add(Helpers1.H1_15(n));   // cross-file project helper
            acc.Add(Helpers2.H2_37(n));   // cross-file project helper
            acc.Add(Helpers1.H1_34(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #8
        /* multi-line note
           describing the routine */
        public int TCF_Svc1_Op8(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            if (n > 0 || n < -0)   // if + ||
            {
                acc.Add(n - 0);
            }
            if (n > 1 || n < -1)   // if + ||
            {
                acc.Add(n - 1);
            }
            for (int i = 0; i < 3; i++)
            {
                acc.Add(i * 3); // inline
            }
            acc.Add(Helpers1.H1_39(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #9
        public int TCF_Svc1_Op9(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            acc.Add(Helpers2.H2_29(n));   // cross-file project helper
            acc.Add(Helpers0.H0_19(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #10
        public int TCF_Svc1_Op10(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            for (int i = 0; i < 1; i++)
            {
                acc.Add(i * 1); // inline
            }
            if (n > 1 || n < -1)   // if + ||
            {
                acc.Add(n - 1);
            }
            for (int i = 0; i < 3; i++)
            {
                acc.Add(i * 3); // inline
            }
            acc.Add(Helpers0.H0_19(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #11
        /* multi-line note
           describing the routine */
        public int TCF_Svc1_Op11(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            for (int i = 0; i < 1; i++)
            {
                acc.Add(i * 1); // inline
            }
            if (n > 1 || n < -1)   // if + ||
            {
                acc.Add(n - 1);
            }
            acc.Add(Helpers2.H2_42(n));   // cross-file project helper
            acc.Add(Helpers1.H1_31(n));   // cross-file project helper
            acc.Add(Helpers0.H0_28(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #12
        /* multi-line note
           describing the routine */
        public int TCF_Svc1_Op12(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            if (n > 0 || n < -0)   // if + ||
            {
                acc.Add(n - 0);
            }
            if (n > 1 || n < -1)   // if + ||
            {
                acc.Add(n - 1);
            }
            for (int i = 0; i < 3; i++)
            {
                acc.Add(i * 3); // inline
            }
            acc.Add(Helpers2.H2_27(n));   // cross-file project helper
            acc.Add(Helpers2.H2_15(n));   // cross-file project helper
            acc.Add(Helpers1.H1_37(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

    }
}
