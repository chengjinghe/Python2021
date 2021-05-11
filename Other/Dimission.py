import time,sys,os

class Dimi():
    Name=None
    Host=None
    Department=None
    Position=None
    Cacuser=None
    Email=None
    RTX=None
    Affirm=None
    Remark=None
    def __init__(self,Name=Name,Host=Host,Department=Department,Position=Department,Cacuser=Cacuser,Email=Email,RTX=RTX,Affirm=Affirm,Remark=Remark):
        self.Name = Name
        self.Host = Host
        self.Department = Department
        self.Position = Position
        self.Cacuser = Cacuser
        self.Email = Email
        self.RTX = RTX
        self.Affirm = Affirm
        self.Remark = Remark
    def dispaly(self):
        print('''已经输入的信息为:
                        1.姓名:{Name}

                        2.电脑IP:{Host}

                        3.部门:{Department}

                        4.职位:{Position}

                        5.CAC帐号:{Cacuser}

                        6.邮箱帐号:{Email}

                        7.腾讯通帐号:{RTX}

                        8.确认办理:{Affirm}

                        9.备注:{Remark}'''.format(Name=self.Name,Host=self.Host,Department=self.Department,Position=self.Position,\
                            Cacuser=self.Cacuser,Email=self.Email,RTX=self.RTX,Affirm=self.Affirm,Remark=self.Remark))
                        
    def start(self): 
        mun = '0'
        while True:
            print('='*100)
            self.dispaly()
            mun = str(input(
        '''请输入序号,然后回车: 
        1.姓名, 2.电脑IP                                       Y.保存
                                                               0.退出
        3.部门, 4.职位, 5.CAC帐号

        6.邮箱帐号, 7.腾讯通帐号, 

        8.确认办理, 9.备注

        ===============>>请输入序号:'''))
            print('='*100)

            if mun=='1':
                self.Name = str(input('请输入离职姓名,默认为空(回车):'))

                print('='*100)
            elif mun=='2':
                self.Host = str(input('请输入电脑IP,默认为空(回车):'))
                print('='*100)
            elif mun=='3':
                self.Department = str(input('请输入部门,默认为空(回车):'))
                print('='*100)
            elif mun=='4':
                self.Position = str(input('请输入职位,默认为空(回车):'))
                print('='*100)
            elif mun=='5':
                self.Cacuser = str(input('请输入CAC帐号,默认为空(回车):'))
                print('='*100)
            elif mun=='6':
                self.Email = str(input('请输入公司邮箱帐号,默认为空(回车):'))
                print('='*100)
            elif mun=='7':
                self.RTX = str(input('请输入腾讯通帐号,默认为空(回车):'))
                print('='*100)
            elif mun=='8':
                self.Affirm = str(input('请输入手续确认办理,默认为空(回车):'))
                print('='*100)
            elif mun=='9':
                self.Remark = str(input('请输入备注,默认为空(回车):'))
                print('='*100)
            elif mun == 'yes' or mun == 'y' or mun == 'Y' or mun == 'YES':
                os.system('cls')
                print('已保存!!!')
                time.sleep(1)          
            elif mun== '0':
                print('='*100)
                break
        return self.Name,self.Host,self.Department,self.Position,\
                            self.Cacuser,self.Email,self.RTX,self.Affirm,self.Remark

 
d = Dimi()
d.start()

