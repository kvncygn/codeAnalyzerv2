using System;
using System.Collections.Generic;

// Auto-generated TCF file #2 (TCF methods only; helpers live elsewhere).
namespace Enterprise
{
    public class Service2
    {
        // TCF entry point #0
        /* multi-line note
           describing the routine */
        public int TCF_Svc2_Op0(int n)
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
            acc.Add(Helpers1.H1_46(n));   // cross-file project helper
            acc.Add(Helpers2.H2_13(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #1
        /* multi-line note
           describing the routine */
        public int TCF_Svc2_Op1(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            for (int i = 0; i < 1; i++)
            {
                acc.Add(i * 1); // inline
            }
            acc.Add(Helpers1.H1_34(n));   // cross-file project helper
            acc.Add(Helpers1.H1_24(n));   // cross-file project helper
            acc.Add(Helpers2.H2_7(n));   // cross-file project helper
            acc.Add(TCF_Svc2_Op0(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #2
        public int TCF_Svc2_Op2(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            acc.Add(Helpers2.H2_21(n));   // cross-file project helper
            acc.Add(Helpers1.H1_30(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #3
        /* multi-line note
           describing the routine */
        public int TCF_Svc2_Op3(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            acc.Add(Helpers1.H1_33(n));   // cross-file project helper
            acc.Add(Helpers0.H0_38(n));   // cross-file project helper
            acc.Add(Helpers1.H1_23(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #4
        public int TCF_Svc2_Op4(int n)
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
            acc.Add(Helpers0.H0_7(n));   // cross-file project helper
            acc.Add(Helpers2.H2_14(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #5
        public int TCF_Svc2_Op5(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            for (int i = 0; i < 1; i++)
            {
                acc.Add(i * 1); // inline
            }
            acc.Add(Helpers2.H2_17(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #6
        public int TCF_Svc2_Op6(int n)
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
            acc.Add(Helpers0.H0_32(n));   // cross-file project helper
            acc.Add(Helpers1.H1_3(n));   // cross-file project helper
            acc.Add(Helpers2.H2_32(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #7
        /* multi-line note
           describing the routine */
        public int TCF_Svc2_Op7(int n)
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
            acc.Add(Helpers2.H2_15(n));   // cross-file project helper
            acc.Add(Helpers1.H1_21(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #8
        public int TCF_Svc2_Op8(int n)
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
            acc.Add(Helpers2.H2_39(n));   // cross-file project helper
            acc.Add(Helpers1.H1_16(n));   // cross-file project helper
            acc.Add(Helpers2.H2_27(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #9
        public int TCF_Svc2_Op9(int n)
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
            acc.Add(Helpers1.H1_47(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #10
        /* multi-line note
           describing the routine */
        public int TCF_Svc2_Op10(int n)
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
            acc.Add(Helpers2.H2_17(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #11
        public int TCF_Svc2_Op11(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            if (n > 0 || n < -0)   // if + ||
            {
                acc.Add(n - 0);
            }
            acc.Add(Helpers0.H0_15(n));   // cross-file project helper
            acc.Add(Helpers2.H2_39(n));   // cross-file project helper
            acc.Add(TCF_Svc2_Op10(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #12
        public int TCF_Svc2_Op12(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            for (int i = 0; i < 1; i++)
            {
                acc.Add(i * 1); // inline
            }
            acc.Add(Helpers1.H1_15(n));   // cross-file project helper
            acc.Add(Helpers0.H0_23(n));   // cross-file project helper
            acc.Add(Helpers1.H1_29(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #13
        public int TCF_Svc2_Op13(int n)
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
            acc.Add(Helpers0.H0_32(n));   // cross-file project helper
            acc.Add(TCF_Svc2_Op12(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #14
        public int TCF_Svc2_Op14(int n)
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
            acc.Add(Helpers2.H2_31(n));   // cross-file project helper
            acc.Add(Helpers2.H2_26(n));   // cross-file project helper
            acc.Add(Helpers1.H1_23(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #15
        /* multi-line note
           describing the routine */
        public int TCF_Svc2_Op15(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            for (int i = 0; i < 1; i++)
            {
                acc.Add(i * 1); // inline
            }
            acc.Add(Helpers0.H0_27(n));   // cross-file project helper
            acc.Add(Helpers2.H2_29(n));   // cross-file project helper
            acc.Add(Helpers0.H0_21(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #16
        /* multi-line note
           describing the routine */
        public int TCF_Svc2_Op16(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            if (n > 0 || n < -0)   // if + ||
            {
                acc.Add(n - 0);
            }
            acc.Add(Helpers1.H1_37(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #17
        public int TCF_Svc2_Op17(int n)
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
            acc.Add(Helpers1.H1_9(n));   // cross-file project helper
            acc.Add(Helpers2.H2_11(n));   // cross-file project helper
            acc.Add(Helpers1.H1_26(n));   // cross-file project helper
            acc.Add(TCF_Svc2_Op16(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

    }
}
