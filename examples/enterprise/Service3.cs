using System;
using System.Collections.Generic;

// Auto-generated TCF file #3 (TCF methods only; helpers live elsewhere).
namespace Enterprise
{
    public class Service3
    {
        // TCF entry point #0
        /* multi-line note
           describing the routine */
        public int TCF_Svc3_Op0(int n)
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
            acc.Add(Helpers1.H1_22(n));   // cross-file project helper
            acc.Add(Helpers2.H2_33(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #1
        public int TCF_Svc3_Op1(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            if (n > 0 || n < -0)   // if + ||
            {
                acc.Add(n - 0);
            }
            acc.Add(Helpers1.H1_38(n));   // cross-file project helper
            acc.Add(Helpers0.H0_14(n));   // cross-file project helper
            acc.Add(TCF_Svc3_Op0(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #2
        public int TCF_Svc3_Op2(int n)
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
            acc.Add(Helpers1.H1_18(n));   // cross-file project helper
            acc.Add(Helpers2.H2_38(n));   // cross-file project helper
            acc.Add(TCF_Svc3_Op1(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #3
        /* multi-line note
           describing the routine */
        public int TCF_Svc3_Op3(int n)
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
            acc.Add(Helpers2.H2_41(n));   // cross-file project helper
            acc.Add(Helpers0.H0_17(n));   // cross-file project helper
            acc.Add(TCF_Svc3_Op2(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #4
        public int TCF_Svc3_Op4(int n)
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
            acc.Add(Helpers1.H1_16(n));   // cross-file project helper
            acc.Add(Helpers1.H1_27(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #5
        /* multi-line note
           describing the routine */
        public int TCF_Svc3_Op5(int n)
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
            acc.Add(Helpers0.H0_14(n));   // cross-file project helper
            acc.Add(Helpers0.H0_37(n));   // cross-file project helper
            acc.Add(Helpers2.H2_12(n));   // cross-file project helper
            acc.Add(TCF_Svc3_Op4(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #6
        /* multi-line note
           describing the routine */
        public int TCF_Svc3_Op6(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            if (n > 0 || n < -0)   // if + ||
            {
                acc.Add(n - 0);
            }
            acc.Add(Helpers0.H0_15(n));   // cross-file project helper
            acc.Add(Helpers1.H1_7(n));   // cross-file project helper
            acc.Add(Helpers2.H2_12(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #7
        public int TCF_Svc3_Op7(int n)
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
            acc.Add(Helpers1.H1_44(n));   // cross-file project helper
            acc.Add(TCF_Svc3_Op6(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #8
        public int TCF_Svc3_Op8(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            if (n > 0 || n < -0)   // if + ||
            {
                acc.Add(n - 0);
            }
            for (int i = 0; i < 2; i++)
            {
                acc.Add(i * 2); // inline
            }
            if (n > 2 || n < -2)   // if + ||
            {
                acc.Add(n - 2);
            }
            acc.Add(Helpers1.H1_44(n));   // cross-file project helper
            acc.Add(Helpers2.H2_25(n));   // cross-file project helper
            acc.Add(TCF_Svc3_Op7(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #9
        /* multi-line note
           describing the routine */
        public int TCF_Svc3_Op9(int n)
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
            acc.Add(Helpers1.H1_13(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #10
        public int TCF_Svc3_Op10(int n)
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
            acc.Add(Helpers2.H2_33(n));   // cross-file project helper
            acc.Add(TCF_Svc3_Op9(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #11
        public int TCF_Svc3_Op11(int n)
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
            acc.Add(Helpers2.H2_17(n));   // cross-file project helper
            acc.Add(TCF_Svc3_Op10(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #12
        public int TCF_Svc3_Op12(int n)
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
            acc.Add(Helpers1.H1_25(n));   // cross-file project helper
            acc.Add(TCF_Svc3_Op11(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #13
        /* multi-line note
           describing the routine */
        public int TCF_Svc3_Op13(int n)
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
            acc.Add(Helpers0.H0_11(n));   // cross-file project helper
            acc.Add(Helpers1.H1_27(n));   // cross-file project helper
            acc.Add(Helpers1.H1_41(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #14
        /* multi-line note
           describing the routine */
        public int TCF_Svc3_Op14(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            acc.Add(Helpers1.H1_19(n));   // cross-file project helper
            acc.Add(TCF_Svc3_Op13(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #15
        public int TCF_Svc3_Op15(int n)
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
            if (n > 2 || n < -2)   // if + ||
            {
                acc.Add(n - 2);
            }
            acc.Add(Helpers2.H2_38(n));   // cross-file project helper
            acc.Add(Helpers0.H0_33(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #16
        /* multi-line note
           describing the routine */
        public int TCF_Svc3_Op16(int n)
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
            acc.Add(Helpers1.H1_20(n));   // cross-file project helper
            acc.Add(Helpers1.H1_43(n));   // cross-file project helper
            acc.Add(Helpers1.H1_41(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #17
        public int TCF_Svc3_Op17(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            acc.Add(Helpers1.H1_10(n));   // cross-file project helper
            acc.Add(Helpers2.H2_12(n));   // cross-file project helper
            acc.Add(Helpers1.H1_0(n));   // cross-file project helper
            acc.Add(TCF_Svc3_Op16(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #18
        /* multi-line note
           describing the routine */
        public int TCF_Svc3_Op18(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            acc.Add(Helpers1.H1_43(n));   // cross-file project helper
            acc.Add(Helpers1.H1_1(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

    }
}
