namespace SunumDemosu 
{
    // USED Definition (Kullanılan Tanım)
    // SiparisServisi.cs içinde "new SiparisModeli" şeklinde kullanıldığı için
    // Dışarıdan DLL'ler eksik olup (Candidate Symbols) hatasına düşse BİLE 
    // yeni güncellememiz sayesinde Unused listesine DÜŞMEYECEKTİR.
    public class SiparisModeli 
    {
        public int Id { get; set; }
    }

    // UNUSED Definition (Class - Kullanılmayan Sınıf)
    // Projenin hiçbir yerinde "new EskiMusteriModeli" denmediği için bu sınıf 
    // "Unused Definitions" sekmesinde gözükecektir.
    public class EskiMusteriModeli 
    {
        // UNUSED Definition (Property - Kullanılmayan Özellik)
        public string Ad { get; set; }
    }

    // UNUSED Definition (Enum - Kullanılmayan Enum)
    // Projenin hiçbir yerinde SiparisDurumu kullanılmadığı için listede çıkacaktır.
    public enum SiparisDurumu 
    {
        Hazirlaniyor,
        Kargoda
    }
}
