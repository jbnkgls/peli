from random import randint, choice
import pygame

class Peli:
    def __init__(self):
        pygame.init()

        self.uusi_peli()

        self.kello = pygame.time.Clock()

        self.leveys, self.korkeus = 1024, 768
        self.ylos, self.alas, self.vas, self.oik = False, False, False, False
        self.m_x, self.m_y = self.leveys/2-self.morko.get_width()/2, self.korkeus/2-self.morko.get_width()
        self.m_suunta_x, self.m_suunta_y, self.k_suunta_x, self.k_suunta_y = 0,0,0,0
        self.k_x, self.k_y = self.leveys/2-self.kolikko.get_width()/2, self.korkeus/2-self.kolikko.get_width()

        self.naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        self.fontti = pygame.font.SysFont("Arial", 24)
        self.fontti_e = pygame.font.SysFont("Arial", 30)
        pygame.display.set_caption("Pakene mörköjä ja kerää kolikoita- peli")

        self.silmukka()

    def lataa_kuvat(self):
        self.robo = pygame.image.load("robo.png")
        self.morko = pygame.image.load("hirvio.png")
        self.ovi = pygame.image.load("ovi.png")
        self.ovi = pygame.transform.rotate(self.ovi, 180)
        self.kolikko = pygame.image.load("kolikko.png")

    def uusi_peli(self):
        self.elamat = 56
        self.x = 100
        self.y = 100
        self.kolikot = []
        self.morot = []
        self.aika, self.laskuri, self.keratyt = 0, 0, 0
        self.robo = pygame.image.load("robo.png")
        self.lataa_kuvat()

    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()
            self.liiku()
            self.morko_lisain()
            self.kolikko_lisain()

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = True
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = True
                if tapahtuma.key == pygame.K_LEFT:
                    self.vas = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oik = True
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_UP:
                    self.ylos = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = False
                if tapahtuma.key == pygame.K_LEFT:
                    self.vas = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oik = False
            if tapahtuma.type == pygame.QUIT:
                exit()

    def liiku(self):

        if self.ylos:
            self.suunta_x, self.suunta_y = 0, -1
            self.kaanto(0)
            self.y -= 4
            if self.y < 0:
                if self.y < 0 - self.robo.get_height()/2:
                    self.y = self.korkeus - self.robo.get_height()/2

        if self.alas:
            self.suunta_x, self.suunta_y = 0, 1
            self.kaanto(180)
            self.y += 4
            if self.y + self.robo.get_height()/2 > self.korkeus:
                self.y = 0 - self.robo.get_height()/2

        if self.vas:
            self.suunta_x, self.suunta_y = -1, 0
            self.kaanto(90)
            self.x -= 4
            if self.x < 0:
                if self.x < 0 - self.robo.get_width()/2:
                    self.x = self.leveys - self.robo.get_width()/2
                    
        if self.oik:
            self.suunta_x, self.suunta_y = 1, 0
            self.kaanto(-90)
            self.x += 4
            if self.x + self.robo.get_width()/2 > self.leveys:
                self.x = 0 - self.robo.get_width()/2

        if self.ylos and self.vas:
            self.suunta_x, self.suunta_y = -1, -1
            self.kaanto(45)

        if self.ylos and self.oik:
            self.suunta_x, self.suunta_y = 1, -1
            self.kaanto(-45)

        if self.alas and self.vas:
            self.suunta_x, self.suunta_y = -1, 1
            self.kaanto(135)

        if self.alas and self.oik:
            self.suunta_x, self.suunta_y = 1, 1
            self.kaanto(-135)

    def kaanto(self, suunta):
        self.robo = pygame.image.load("robo.png")
        self.robo = pygame.transform.rotate(self.robo, suunta)

    def ajastin(self):
        if self.laskuri < 60:
            self.laskuri += 1
        else:
            self.aika += 1
            self.laskuri = 0

    def kolikko_lisain(self):
        if randint(1,200) == 1:
            if self.x <= self.k_x:
                self.k_suunta_x = -1
            else:
                self.k_suunta_x = 1
            if self.y <= self.k_y:
                self.k_suunta_y = -1
            else:
                self.k_suunta_y = 1
            self.kolikot.append([self.k_x, self.k_y, self.k_suunta_x, self.k_suunta_y])

    def morko_lisain(self):
        if randint(1,80) == 1:
            if self.x <= self.m_x:
                self.m_suunta_x = -1
            else:
                self.m_suunta_x = 1
            if self.y <= self.m_y:
                self.m_suunta_y = -1
            else:
                self.m_suunta_y = 1
            self.morot.append([self.m_x, self.m_y, self.m_suunta_x, self.m_suunta_y])

    def piirra_kolikot(self):
        for i in range(len(self.kolikot)):     
            if self.x <= self.kolikot[i][0]:
                self.kolikot[i][2] = 1
            else:
                self.kolikot[i][2] = -1
            if self.y <= self.kolikot[i][1]:
                self.kolikot[i][3] = 1
            else:
                self.kolikot[i][3] = -1
            if self.osuma_kolikko(self.kolikot[i][0],self.kolikot[i][1]):
                self.kolikot[i][0] += self.kolikot[i][2] * 11001
                self.kolikot[i][1] += self.kolikot[i][3] * 10011
            self.kolikot[i][0] += self.kolikot[i][2] * 1
            self.kolikot[i][1] += self.kolikot[i][3] * 1
            self.naytto.blit(self.kolikko, (self.kolikot[i][0], self.kolikot[i][1]))

    def piirra_morot(self):
        for i in range(len(self.morot)):
            if self.x <= self.morot[i][0]:
                self.morot[i][2] = choice([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1])
            else:
                self.morot[i][2] = choice([-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
            if self.y <= self.morot[i][1]:
                self.morot[i][3] = choice([-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,1])
            else:
                self.morot[i][3] = choice([-1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
            if self.osuma_morko(self.morot[i][0],self.morot[i][1]):
                self.morot[i][0] += self.morot[i][2] * -100
                self.morot[i][1] += self.morot[i][3] * -100
            self.morot[i][0] += self.morot[i][2] * choice([2,3,4])
            self.morot[i][1] += self.morot[i][3] * choice([2,3,4])
            self.naytto.blit(self.morko, (self.morot[i][0], self.morot[i][1]))

    def osuma_morko(self,x, y):
        robo = pygame.sprite.Sprite()
        robo.rect = pygame.Rect(self.x, self.y, self.robo.get_width(), self.robo.get_height())
        morko = pygame.sprite.Sprite()
        morko.rect = pygame.Rect(x,y,self.morko.get_width(), self.morko.get_height())
        if pygame.sprite.collide_rect(robo, morko):
            self.elama(-1)
            return True

    def osuma_kolikko(self,x, y):
        robo = pygame.sprite.Sprite()
        robo.rect = pygame.Rect(self.x, self.y, self.robo.get_width(), self.robo.get_height())
        kolikko = pygame.sprite.Sprite()
        kolikko.rect = pygame.Rect(x,y,self.kolikko.get_width(), self.kolikko.get_height())
        if pygame.sprite.collide_rect(robo, kolikko):
            self.elama(1)
            self.keratyt += 1
            return True

    def elama(self, maara):
        if maara > 0:
            if self.elamat < 56:
                self.elamat += maara
        else:
            self.elamat += maara

    def piirra_naytto(self):
        self.naytto.fill((0, 0, 255))
        if not self.kuolema():
            self.naytto.blit(self.ovi, (self.leveys/2-self.ovi.get_width()/2, self.korkeus/2-self.ovi.get_width()))
            self.piirra_morot()
            self.piirra_kolikot()
            self.naytto.blit(self.robo, (self.x,self.y))
            self.naytto.blit(self.robo, (self.x-self.leveys,self.y))
            self.naytto.blit(self.robo, (self.x,self.y-self.korkeus))
            self.naytto.blit(self.robo, (self.x+self.leveys,self.y))
            self.naytto.blit(self.robo, (self.x,self.y+self.korkeus))
            self.naytto.blit(self.robo, (self.x+self.leveys,self.y+self.korkeus))
            self.ajastin()

        teksti = self.fontti_e.render((self.elamat * "♥"), True, (255, 0, 0))
        self.naytto.blit(teksti, (10, 0))

        teksti = self.fontti.render("F2 = uusi peli", True, (255, 0, 0))
        self.naytto.blit(teksti, (5, self.korkeus  - 30))

        teksti = self.fontti.render("Esc = sulje peli", True, (255, 0, 0))
        self.naytto.blit(teksti, (self.leveys-teksti.get_width()-5, self.korkeus  - 30))

        if self.kuolema():
            teksti = self.fontti.render("Hupsista, elämät pääsivät loppumaan!", True, (255, 0, 0))
            teksti_x = self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x, teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))
            teksti_a = self.fontti.render(f"Pysyit hengissä {self.aika} sekunnin ajan ja keräsit {self.keratyt} kolikkoa", True, (255, 0, 0))
            teksti_x_a = self.leveys / 2 - teksti_a.get_width() / 2
            teksti_y_a = self.korkeus / 2 - teksti_a.get_height() / 2 + teksti.get_height()
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x_a, teksti_y_a, teksti_a.get_width(), teksti_a.get_height()))
            self.naytto.blit(teksti_a, (teksti_x_a, teksti_y_a))

        pygame.display.flip()
        self.kello.tick(60)

    def kuolema(self):
        if self.elamat <= 0:
            return True
        return False

if __name__ == "__main__":
    Peli()
