using System;

namespace SunumDemosu
{
    public class ComplexNestedHelpers
    {
        // -----------------------------------------------------
        // TCF (TEST) METOTLARI
        // -----------------------------------------------------

        public void TCF_BankaTransferi()
        {
            BakiyeKontrolEt();
            TransferiGerceklestir();
            TransferLoguYaz();
        }

        public void TCF_KrediKartiOdeme()
        {
            KartGecerlilikKontrolu();
            TransferiGerceklestir();
            TransferLoguYaz(); // 3. TCF çağrısı eklendi
        }

        public void TCF_HesapOzetiSorgula()
        {
            VeritabanindanVeriCek();
            TransferLoguYaz(); // Log işlemini o da kullanıyor
        }

        // -----------------------------------------------------
        // SEVİYE 1 (LEVEL 1) HELPER'LAR
        // -----------------------------------------------------

        private void BakiyeKontrolEt()
        {
            VeritabanindanVeriCek();
            HesaplaLimitler();
        }

        private void KartGecerlilikKontrolu()
        {
            UzakSunucuylaHaberles();
        }

        private void TransferiGerceklestir()
        {
            VeritabanindanVeriCek();
            GuvenlikTaramasiYap();
        }

        private void TransferLoguYaz()
        {
            FormatlaVeYaz();
        }

        // -----------------------------------------------------
        // SEVİYE 2 (LEVEL 2) HELPER'LAR
        // -----------------------------------------------------

        private void VeritabanindanVeriCek()
        {
            BaglantiKur();
            SorguCalistir();
        }

        private void HesaplaLimitler()
        {
            // Sadece matematiksel bir işlem yapıyor
            int x = 5 * 10;
        }

        private void UzakSunucuylaHaberles()
        {
            BaglantiKur();
            SifrelemeYap();
        }

        private void GuvenlikTaramasiYap()
        {
            SifrelemeYap();
            ZararliYazilimTaramasi();
        }

        private void FormatlaVeYaz()
        {
            ZamanDamgasiEkle();
            DosyayaKaydet();
        }

        // -----------------------------------------------------
        // SEVİYE 3 (LEVEL 3) HELPER'LAR (En Derin Katman)
        // -----------------------------------------------------

        private void BaglantiKur()
        {
            // Çok fazla yerden çağrılan (VeritabanindanVeriCek, UzakSunucuylaHaberles) temel metot
        }

        private void SorguCalistir()
        {
        }

        private void SifrelemeYap()
        {
            // UzakSunucuylaHaberles ve GuvenlikTaramasiYap tarafından çağrılıyor
        }

        private void ZararliYazilimTaramasi()
        {
        }

        private void ZamanDamgasiEkle()
        {
        }

        private void DosyayaKaydet()
        {
            BaglantiKur(); // 3. Helper çağrısı eklendi
        }

        // -----------------------------------------------------
        // HİÇBİR TEST (TCF) TARAFINDAN ÇAĞRILMAYAN (UNUSED) METOTLAR
        // -----------------------------------------------------

        private void EskiLogSistemi()
        {
            // Bu metot başka bir Unused metodu çağırıyor
            EskiDosyayaYaz();
        }

        private void EskiDosyayaYaz()
        {
            BaglantiKur(); // 4. Helper çağrısı eklendi (Fakat Unused grafından ulaşıldığı için TCF grafında görünmeyecek, bu yüzden sadece 3 helper çağrısı görülecek)
        }
    }
}
