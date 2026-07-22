using System;
using System.Collections.Generic;

// Auto-generated TCF file #0 (TCF methods only; helpers live elsewhere).
namespace Enterprise
{
    public class Service0
    {
        // TCF entry point #0
        public int TCF_Svc0_Op0(int n)
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
            for (int i = 0; i < 3; i++)
            {
                acc.Add(i * 3); // inline
            }
            acc.Add(Helpers1.H1_30(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #1
        public int TCF_Svc0_Op1(int n)
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
            acc.Add(Helpers1.H1_11(n));   // cross-file project helper
            acc.Add(Helpers2.H2_26(n));   // cross-file project helper
            acc.Add(TCF_Svc0_Op0(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #2
        /* multi-line note
           describing the routine */
        public int TCF_Svc0_Op2(int n)
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
            acc.Add(Helpers1.H1_37(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #3
        public int TCF_Svc0_Op3(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            for (int i = 0; i < 1; i++)
            {
                acc.Add(i * 1); // inline
            }
            acc.Add(Helpers2.H2_5(n));   // cross-file project helper
            acc.Add(Helpers0.H0_36(n));   // cross-file project helper
            acc.Add(Helpers1.H1_24(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #4
        public int TCF_Svc0_Op4(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            for (int i = 0; i < 1; i++)
            {
                acc.Add(i * 1); // inline
            }
            acc.Add(Helpers2.H2_13(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #5
        /* multi-line note
           describing the routine */
        public int TCF_Svc0_Op5(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            if (n > 0 || n < -0)   // if + ||
            {
                acc.Add(n - 0);
            }
            acc.Add(Helpers2.H2_43(n));   // cross-file project helper
            acc.Add(Helpers2.H2_15(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #6
        /* multi-line note
           describing the routine */
        public int TCF_Svc0_Op6(int n)
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
            acc.Add(Helpers2.H2_29(n));   // cross-file project helper
            acc.Add(Helpers2.H2_24(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #7
        public int TCF_Svc0_Op7(int n)
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
            acc.Add(Helpers0.H0_26(n));   // cross-file project helper
            acc.Add(TCF_Svc0_Op6(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #8
        /* multi-line note
           describing the routine */
        public int TCF_Svc0_Op8(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            if (n > 0 || n < -0)   // if + ||
            {
                acc.Add(n - 0);
            }
            acc.Add(Helpers2.H2_20(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #9
        public int TCF_Svc0_Op9(int n)
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
            acc.Add(Helpers2.H2_38(n));   // cross-file project helper
            acc.Add(Helpers1.H1_43(n));   // cross-file project helper
            acc.Add(Helpers0.H0_22(n));   // cross-file project helper
            acc.Add(TCF_Svc0_Op8(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #10
        public int TCF_Svc0_Op10(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            if (n > 0 || n < -0)   // if + ||
            {
                acc.Add(n - 0);
            }
            acc.Add(Helpers1.H1_28(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #11
        public int TCF_Svc0_Op11(int n)
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
            acc.Add(Helpers1.H1_27(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #12
        public int TCF_Svc0_Op12(int n)
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
            acc.Add(Helpers0.H0_33(n));   // cross-file project helper
            acc.Add(Helpers0.H0_11(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #13
        /* multi-line note
           describing the routine */
        public int TCF_Svc0_Op13(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            acc.Add(Helpers1.H1_27(n));   // cross-file project helper
            acc.Add(TCF_Svc0_Op12(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #14
        /* multi-line note
           describing the routine */
        public int TCF_Svc0_Op14(int n)
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
            acc.Add(Helpers1.H1_34(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #15
        public int TCF_Svc0_Op15(int n)
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
            acc.Add(Helpers0.H0_9(n));   // cross-file project helper
            acc.Add(Helpers0.H0_3(n));   // cross-file project helper
            acc.Add(TCF_Svc0_Op14(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #16
        public int TCF_Svc0_Op16(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            for (int i = 0; i < 1; i++)
            {
                acc.Add(i * 1); // inline
            }
            acc.Add(Helpers2.H2_26(n));   // cross-file project helper
            acc.Add(TCF_Svc0_Op15(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #17
        public int TCF_Svc0_Op17(int n)
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
            for (int i = 0; i < 3; i++)
            {
                acc.Add(i * 3); // inline
            }
            acc.Add(Helpers1.H1_38(n));   // cross-file project helper
            acc.Add(Helpers1.H1_15(n));   // cross-file project helper
            acc.Add(Helpers1.H1_18(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #18
        public int TCF_Svc0_Op18(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            if (n > 0 || n < -0)   // if + ||
            {
                acc.Add(n - 0);
            }
            acc.Add(Helpers0.H0_13(n));   // cross-file project helper
            acc.Add(Helpers0.H0_33(n));   // cross-file project helper
            acc.Add(TCF_Svc0_Op17(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #19
        public int TCF_Svc0_Op19(int n)
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
            acc.Add(Helpers2.H2_9(n));   // cross-file project helper
            acc.Add(Helpers2.H2_41(n));   // cross-file project helper
            acc.Add(Helpers1.H1_32(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #20
        public int TCF_Svc0_Op20(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            acc.Add(Helpers1.H1_7(n));   // cross-file project helper
            acc.Add(Helpers1.H1_0(n));   // cross-file project helper
            acc.Add(TCF_Svc0_Op19(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #21
        /* multi-line note
           describing the routine */
        public int TCF_Svc0_Op21(int n)
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
            acc.Add(Helpers1.H1_42(n));   // cross-file project helper
            acc.Add(Helpers1.H1_22(n));   // cross-file project helper
            acc.Add(Helpers0.H0_8(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #22
        /* multi-line note
           describing the routine */
        public int TCF_Svc0_Op22(int n)
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
            acc.Add(Helpers2.H2_33(n));   // cross-file project helper
            acc.Add(TCF_Svc0_Op21(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #23
        public int TCF_Svc0_Op23(int n)
        {
            var acc = new List<int>();
            acc.Add(n);                 // library List.Add -> NOT a helper
            for (int i = 0; i < 1; i++)
            {
                acc.Add(i * 1); // inline
            }
            acc.Add(Helpers0.H0_23(n));   // cross-file project helper
            acc.Add(TCF_Svc0_Op22(n - 1));  // TCF->TCF, must be ignored
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

        // TCF entry point #24
        /* multi-line note
           describing the routine */
        public int TCF_Svc0_Op24(int n)
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
            acc.Add(Helpers1.H1_19(n));   // cross-file project helper
            acc.Add(Helpers0.H0_21(n));   // cross-file project helper
            acc.Add(Helpers2.H2_47(n));   // cross-file project helper
            int total = 0;
            foreach (var v in acc) { total += v; }
            return total;
        }

    }
}
