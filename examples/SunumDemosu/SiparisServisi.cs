using System;
// Bilerek var olmayan bir kütüphane ekledik ki "Candidate Symbols" (Aday Semboller) 
// çözümümüzün nasıl işe yaradığını ve DLL hatasında çökmediğini görelim.
using External.Unknown.Library; 

namespace SunumDemosu 
{
    public class SiparisServisi 
    {
        // 1. TCF Metodu
        public void TCF_SiparisOlustur_Basarili() 
        {
            // Proje içi Helper çağrısı
            VeritabaninaKaydet();
            
            // Başka bir sınıftaki Helper çağrısı
            YardimciAraclar.LogYaz("Sipariş oluşturuldu.");

            // KAPSAMLI KARMAŞIKLIK (COMPLEXITY) TESTİ:
            // 1. Standart 'if' kullanımı (Complexity +1)
            int siparisAdedi = 5;
            if (siparisAdedi > 0) 
            {
                // 2. Yeni kural: 'or' pattern (Complexity +1)
                if (siparisAdedi is 5 or 10) 
                {
                    // 3. Yeni kural: '?.' Null conditional (Complexity +1)
                    SiparisModeli testModel = null;
                    int? id = testModel?.Id; 
                }
            }
            // Beklenen Complexity: 1 (Kendi) + 3 (Dallanmalar) = 4
        }

        // 2. TCF Metodu
        public void TCF_SiparisIptal_Basarili() 
        {
            YardimciAraclar.LogYaz("Sipariş iptal edildi.");

            // Dış DLL (C# BCL veya eklenti) çağrısı. 
            // Bu çağrı "Helper" listesine girmeyecektir çünkü kaynak kodda değil!
            Console.WriteLine("Sistem logu");
        }

        // Helper Metot (TCF_SiparisOlustur_Basarili tarafından çağrıldığı için Helper listesine girer)
        private void VeritabaninaKaydet() 
        {
            // Sınıf kullanımı ("SiparisModeli" sınıfı ve "Id" özelliği USED olarak işaretlenir)
            // Eğer dll bulunamazsa Candidate Symbols sayesinde yine de USED sayılacak.
            var siparis = new SiparisModeli { Id = 1 };
        }
    }
}
