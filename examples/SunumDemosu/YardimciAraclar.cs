using System;

namespace SunumDemosu 
{
    public class YardimciAraclar 
    {
        // TCF_SiparisOlustur ve TCF_SiparisIptal metotları bunu doğrudan çağırıyor.
        // Bu yüzden "Helper" sekmesinde bu metot yeşil rozetle çıkacaktır.
        public static void LogYaz(string mesaj) 
        {
            // Yeni kural: '??=' (Coalesce assignment) -> Complexity +1
            mesaj ??= "Boş Mesaj"; 

            Console.WriteLine(mesaj); 
            FormatlaLog(mesaj); 
        }

        // TCF metodu değil HELPER metodu çağırıyor! 
        // Sistemin "sadece TCF'nin direkt çağırdıklarını baz al" mantığı yüzünden
        // Bu metot "Unused Methods (Kullanılmayan Metotlar)" listesinde gözükecektir.
        private static void FormatlaLog(string mesaj) 
        {
            // log formatlama kodları
        }

        // TCF tarafından VEYA Helper tarafından ÇAĞRILMAYAN tamamen izole metot.
        // Bu da "Unused Methods" sekmesinde çıkacaktır.
        public void KullanilmayanMetot() 
        {
        }
    }
}
