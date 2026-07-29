using System;

namespace SunumDemosu 
{
    public class TimeComplexityDemosu 
    {
        // 1. O(1) - Sabit Zaman (Döngü yok)
        public void Demo_SabitZaman_O1()
        {
            int a = 5;
            int b = 10;
            Console.WriteLine(a + b);
        }

        // 2. O(N) - Lineer Zaman (Tek döngü)
        public void Demo_LineerZaman_ON()
        {
            for (int i = 0; i < 100; i++)
            {
                Console.WriteLine("İşlem: " + i);
            }
        }

        // 3. O(N^2) - Karesel Zaman (İç içe 2 döngü)
        public void Demo_KareselZaman_ON2()
        {
            for (int i = 0; i < 10; i++)
            {
                int j = 0;
                while (j < 5)
                {
                    Console.WriteLine($"i: {i}, j: {j}");
                    j++;
                }
            }
        }

        // 4. O(N^3) - Kübik Zaman (İç içe 3 döngü)
        public void Demo_KubikZaman_ON3()
        {
            for (int i = 0; i < 10; i++)
            {
                for (int j = 0; j < 5; j++)
                {
                    for (int k = 0; k < 2; k++)
                    {
                        Console.WriteLine("Derin döngü...");
                    }
                }
            }
        }
    }
}
