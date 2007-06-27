from bookmark import *

class UserMigration:
    def __init__(self, partition, parttype, userdir):
        self.sources = {}
        self.options = {}
        # Desteklenen programlarin yuklu olup olmadigina bak, yukluyse hangi dizinde olduklarini bul.
        # "Masaustu", "Belgelerim", "Muziklerim" gibi dizinleri bul. Boyutlarini kaydet.
        # Hangi sistem ayarlarinin yapilabildigine bak.
        # Tum bulduklarini "sources" sozlugune kaydet
        widget = OptionsWidget(self.sources, self.options)
        self.Apply()
    
    def Apply(self):
        # Options sozlugundeki seceneklerin uzerinden gecerek yapilmasi istenen islemleri sirayla uygula
        # firefox vb programlar aciksa uyari ver
        pass

class OptionsWidget:
    def __init__(self, sources, options):
        # sources'ta bulunan secenekleri soran bir widget goster
        # Bu widget'i kullarak aldigin cevaplari "options" sozlugune kaydet
        pass
