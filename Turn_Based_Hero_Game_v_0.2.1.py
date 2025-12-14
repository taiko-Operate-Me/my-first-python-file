import random
import os
import time
class Character: 
    def __init__(self, name="NonamedChar", hp=1, mp=1, attack=1, defense=0): 
        self.name=name 
        self.max_hp=hp 
        self.max_mp=mp 
        self.current_hp=hp 
        self.current_mp=mp
        self.basic_attack=attack
        self.attack=attack 
        self.defense=defense 
        self.action=None 
    def show_status(self): 
        print(f"이름: {self.name}\n체력: {self.current_hp}/{self.max_hp}\n마나: {self.current_mp}/{self.max_mp}\n공격력/방어력: {self.attack}/{self.defense}") 
    def choose_action(self): 
        self.action='attack' 
    def calc_effective_attack(self, opponent): 
        return int(self.attack*10/(10+opponent.defense)) 
    def is_alive(self): 
        return self.current_hp>0 
    def take_damage(self, damage): 
        self.current_hp-=damage 
        if self.current_hp<0: 
            self.current_hp=0 
#여기부터 ChatGPT가 도와줌
class Skill:
    @staticmethod
    def shield(user, target):
        if user.current_mp>=50:
            user.current_mp-=50
            print(f"{user.name}이(가) 마법 방패를 소환해 피해를 방어했습니다!(최종 피해 1/2)")
            user.action="shield"
        else:
            print(f"{user.name}이(가) 마법 방패 스킬을 사용했지만 mp가 부족합니다. {user.name}은(는) 이번 턴에 아무 행동도 하지 않습니다.")
            user.action = None
    @staticmethod
    def slash(user, target):
        if user.current_mp>=20:
            user.current_mp-=20
            print(f"{user.name}이(가) 당신을 강하게 베었습니다!(최종 피해 1.2배)")
            user.action="slash"
        else:
            print(f"{user.name}이(가) 베기 스킬을 사용했지만 mp가 부족합니다. {user.name}은(는) 이번 턴에 아무 행동도 하지 않습니다.")
            user.action = None
    @staticmethod
    def stab(user, target):
        if user.current_mp>=30:
            user.current_mp-=30
            print(f"{user.name}이(가) 당신을 강하게 찔렀습니다!(최종 피해 1.5배)")
            user.action="stab"
        else:
            print(f"{user.name}이(가) 찌르기 스킬을 사용했지만 mp가 부족합니다. {user.name}은(는) 이번 턴에 아무 행동도 하지 않습니다.")
            user.action = None
    @staticmethod
    def anger(user, target):
        if user.current_mp>=50:
            user.current_mp-=50
            user.attack+=50
            user.action="anger"
            print(f"{user.name}이(가) 분노합니다!(기본 공격력 +50)")
        else:
            print(f"{user.name}이(가)분노 스킬을 사용했지만 mp가 부족합니다. {user.name}은(는) 이번 턴에 아무 행동도 하지 않습니다.")
            user.action = None
#여기까지 ChatGPT가 도와줌
class Hero1(Character): 
    def choose_action(self): 
        while(True): 
            a=input("이번 턴에 수행할 행동을 결정하세요(A: 공격, D: 방어, G: 성장(mp 20 소모, 공격력 +10)): ") 
            if not a: 
                print("부적절한 키 입력입니다.") 
                continue 
            if a[0]=='a' or a[0]=='A': 
                self.action="attack" 
                break 
            elif a[0]=='d' or a[0]=='D': 
                self.action="defense" 
                break 
            elif a[0]=='g' or a[0]=='G': 
                self.grow_attack() 
                break 
            else: 
                print("부적절한 키 입력입니다.") 
    def grow_attack(self): 
        if self.current_mp>=20: 
            self.current_mp-=20 
            self.action="grow_attack" 
        else: 
            print("mp가 부족합니다! 이번 턴은 아무 행동도 하지 않습니다.") 
            self.action=None 
    def attack_up(self, atk): 
        self.attack+=atk
        
class Enemy(Character): 
    #여기부터 ChatGPT가 도와줌
    def __init__(self, name, hp, mp, attack, defense, skills=None):
        super().__init__(name, hp, mp, attack, defense)
        self.skills = skills or []
    def use_skill(self, target):
        if not self.skills:
             print(f"{self.name}은(는) 사용할 스킬이 없습니다.")
             self.action = None
             return
        skill_func=random.choice(self.skills) 
        skill_func(self, target)
    def choose_action(self, hero): 
        actions_list=["attack","defense","skill"]
        choice=random.choice(actions_list)
        if choice=="attack":
            self.action="attack"
        elif choice=="defense":
            self.action="defense"
        elif choice=="skill":
            self.use_skill(hero)
        print(f"{self.name}의 행동: {self.action}")
     #여기까지 ChatGPT가 도와줌
def count_turn(turn): 
    print(f"\n현재 턴: {turn}") 
def action_phase(hero,enemy): 
    hero.choose_action() 
    enemy.choose_action(hero) 
def fighting_phase(hero, enemy): 
    ha=hero.action
    ea=enemy.action
    A=hero.calc_effective_attack(enemy)
    B=enemy.calc_effective_attack(hero)
    if ha=="attack":
        if ea=="attack":
            hero.take_damage(B)
            enemy.take_damage(A)
        elif ea=="defense":
            hero.take_damage(10)
            enemy.take_damage(int(A/1.5))
        elif ea=="shield":
            enemy.take_damage(int(A/2))
        elif ea=="slash":
            hero.take_damage(int(B*1.2))
            enemy.take_damage(A)
        elif ea=="stab":
            hero.take_damage(int(B*1.5))
            enemy.take_damage(A)
        else:
            enemy.take_damage(A)
    elif ha=="defense":
        if ea=="attack":
            hero.take_damage(int(B/1.5))
            enemy.take_damage(10)
        elif ea=="defense":
            hero.take_damage(20)
            enemy.take_damage(20)
        elif ea=="shield":
            enemy.take_damage(5) #10/2
        elif ea=="slash":
            hero.take_damage(int(B*0.8)) #B*1.2/1.5
            enemy.take_damage(10)
        elif ea=="stab":
            hero.take_damage(int(B)) #B*1.5/1.5
            enemy.take_damage(10)
        else:
            pass
    elif ha=="grow_attack":
        if ea=="attack":
            hero.take_damage(int(B))
            hero.attack_up(10)
        elif ea=="defense":
            hero.attack_up(10)
        elif ea=="shield":
            hero.attack_up(10)
        elif ea=="slash":
            hero.take_damage(int(B*1.2))
            hero.attack_up(10)
        elif ea=="stab":
            hero.take_damage(int(B*1.5))
            hero.attack_up(10)
        else:
            hero.attack_up(10)
    else:
        if ea=="attack":
            hero.take_damage(B)
        elif ea=="defense":
            pass
        elif ea=="shield":
            pass
        elif ea=="slash":
            hero.take_damage(int(B*1.2))
        elif ea=="stab":
            hero.take_damage(int(B*1.5))
        else:
            pass
def preparing_phase(hero):
    print("포인트 5를 받았습니다! 원하는 능력치에 투자해주세요!")
    print("포인트 1당: 최대 체력 +100, 기본 공격력 +15, 방어력 +1")
    point=5
    while point>0:
        a=input("기본 공격력(A), 방어력(D), 최대 체력(H): ")
        if not a: 
            print("부적절한 키 입력입니다.") 
            continue 
        if a[0]=='a' or a[0]=='A': 
            hero.basic_attack+=15
        elif a[0]=='d' or a[0]=='D': 
            hero.defense+=1
        elif a[0]=='h' or a[0]=='H': 
            hero.max_hp+=100
        else: 
            print("부적절한 키 입력입니다.")
            continue
        point-=1
def show_battle_stats(hero,enemy): 
    print(f"{hero.name}의 남은 체력: {hero.current_hp}, {enemy.name}의 남은 체력: {enemy.current_hp}") 
    print(f"{hero.name}의 남은 마나: {hero.current_mp}, {enemy.name}의 남은 마나: {enemy.current_mp}") 
    print(f"{hero.name}의 현재 공격력: {hero.attack}, {enemy.name}의 현재 공격력: {enemy.attack}") 
    print(f"{hero.name}의 현재 방어력: {hero.defense}, {enemy.name}의 현재 방어력: {enemy.defense}") 
def battle(hero, enemy): 
    hero.current_hp=hero.max_hp
    hero.current_mp=hero.max_mp
    hero.attack=hero.basic_attack
    print(f"{hero.name}와 {enemy.name}의 전투를 시작합니다.") 
    show_battle_stats(hero,enemy)
    turn=1
    while(True): 
        count_turn(turn) 
        action_phase(hero,enemy) 
        fighting_phase(hero, enemy) 
        show_battle_stats(hero,enemy) 
        if not hero.is_alive() and not enemy.is_alive(): 
            print(f"{enemy.name}은(는) 죽었지만 당신도 사망하였습니다.") 
            time.sleep(2.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            return "Game Over"
        elif not hero.is_alive(): 
            print(f"{enemy.name}의 승리입니다.") 
            time.sleep(2.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            return "Game Over"
        elif not enemy.is_alive():
            print(f"{hero.name}의 승리입니다!") 
            time.sleep(2.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            return "Continue!"
        turn+=1
#여기부터 메인 게임 코드
max_hp_plus_500=False
attack_plus_50=False
defense_plus_3=False
print("TBHG v 0.2.1에 오신 것을 환영합니다.")
while(True): 
    a=input("게임을 시작하려면 S키를 누르고 Enter키를 누르세요: ")
    if not a: 
        print("반드시 S키를 누른 뒤 Enter키를 눌러야 진행이 가능합니다.") 
        continue 
    if a=="Health":
        print("숨겨진 포션을 찾았습니다! 영웅의 시작 최대 체력이 500 증가합니다.")
        max_hp_plus_500=True
        continue
    elif a=="Attack":
        print("숨겨진 검을 찾았습니다! 영웅의 시작 기본 공격력이 50 증가합니다.")
        attack_plus_50=True
        continue
    elif a=="Defense":
        print("숨겨진 갑옷을 찾았습니다! 영웅의 시작 방어력이 3 증가합니다.")
        defense_plus_3=True
        continue
    elif a=="s" or a=="S":
        break
    else: 
        continue
hero=Hero1("Hero1", 1000+int(max_hp_plus_500)*500, 100, 100+int(attack_plus_50)*50, 2+int(defense_plus_3)*3)
enemy1=Enemy("Goblin", 1000, 100, 150, 0, [Skill.shield, Skill.slash])
result1=battle(hero,enemy1)
if result1=="Continue!":
    preparing_phase(hero)
    enemy2=Enemy("Skeleton", 750, 0, 250, 0)
    result2=battle(hero,enemy2)
    if result2=="Continue!":
        preparing_phase(hero)
        enemy3=Enemy("Orc", 1200, 100, 200, 1, [Skill.slash, Skill.stab])
        result3=battle(hero,enemy3)
        if result3=="Continue!":
            print("축하드립니다. TBHG v 0.2.1을 클리어하셨습니다!")
            if max_hp_plus_500==True and attack_plus_50==True and defense_plus_3==True:
                final_stage=random.choice([True,True,True,True,False])
            else:
                final_stage=random.choice([True,False,False,False,False])
            if final_stage==True:
                print("\n...인 줄 알았는데?")
                print("갑자기 Dragon이 살벌한 기세로 날아온다!!!")
                enemy4=Enemy("Dragon", 3000, 1000, 250, 3, [Skill.anger])
                result4=battle(hero,enemy4)
                if result4=="Continue!":
                    print("축하드립니다! Dragon을 쓰러뜨리고 TBHG v 0.2.1의 진정한 끝에 도달했습니다!")
                    print("플레이해주셔서 감사드립니다!")
                    #The End
                else:
                    if max_hp_plus_500==False or attack_plus_50==False or defense_plus_3==False:
                        print("내 Health, Attack, Defense가 더 강했더라면...")
                    print("???에서 패배")
            else:
                pass
        else:
            print("3번째 전투에서 패배")
    else:
        print("2번째 전투에서 패배")
else:
    print("1번째 전투에서 패배")