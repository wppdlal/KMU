import pymysql
from PyQt5.QtWidgets import *
import sys, datetime
import csv
import json
import xml.etree.ElementTree as ET

################################################################################################db 출입

class DB_Utils:

    def queryExecutor(self, db, sql, params):
        conn = pymysql.connect(host='localhost', user='guest', password='bemyguest', db=db, charset='utf8')

        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor: 
                cursor.execute(sql, params)
                rows = cursor.fetchall()
                return rows
        except Exception as e:
            print(e)
            print(type(e))
        finally:
            conn.close()
            
########################################################################################### db 검색문

class DB_Queries:
    # 모든 검색문은 여기에 각각 하나의 메소드로 정의

    def selectPlayerPosition(self):
        sql = '''
        SELECT DISTINCT customerid 
        FROM customers
        order by customerid
        '''
        params = ()

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows
    
    def selectPlayerUsingPosition(self, value):
        if value == 'ALL':
            sql = '''
            SELECT o.orderNo, o.orderDate, o.requiredDate, o.shippedDate, o.status, c.name, o.comments
            FROM customers c join orders o on c.customerid=o.customerid
            order by o.orderNo
            '''
            params = ()
        else:
            sql = '''
            SELECT o.orderNo, o.orderDate, o.requiredDate, o.shippedDate, o.status, c.name, o.comments
            FROM customers c join orders o on c.customerid=o.customerid
            WHERE o.customerid = %s
            order by o.orderNo
            '''
            params = (value)         # SQL문의 실제 파라미터 값의 튜플

        util = DB_Utils()
        rows = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows
    
    def selectCountry(self):
        sql = '''
        SELECT DISTINCT country 
        FROM customers
        order by country
        '''
        params = ()

        util = DB_Utils()
        rows1 = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows1
    
    def selectUsingCountry(self, value):
        if value == 'ALL':
            sql = '''
            SELECT o.orderNo, o.orderDate, o.requiredDate, o.shippedDate, o.status, c.name, o.comments
            FROM customers c join orders o on c.customerid=o.customerid
            order by o.orderNo
            '''
            params = ()
        else:
            sql = '''
            SELECT o.orderNo, o.orderDate, o.requiredDate, o.shippedDate, o.status, c.name, o.comments
            FROM customers c join orders o on c.customerid=o.customerid
            WHERE c.country = %s
            order by o.orderNo
            '''
            params = (value)         # SQL문의 실제 파라미터 값의 튜플

        util = DB_Utils()
        rows1 = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows1
    
    def selectCity(self):
        sql = '''
        SELECT DISTINCT city 
        FROM customers
        order by city
        '''
        params = ()

        util = DB_Utils()
        rows2 = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows2
    
    def selectUsingCity(self, value):
        if value == 'ALL':
            sql = '''
            SELECT o.orderNo, o.orderDate, o.requiredDate, o.shippedDate, o.status, c.name, o.comments
            FROM customers c join orders o on c.customerid=o.customerid
            order by o.orderNo
            '''
            params = ()
        else:
            sql = '''
            SELECT o.orderNo, o.orderDate, o.requiredDate, o.shippedDate, o.status, c.name, o.comments
            FROM customers c join orders o on c.customerid=o.customerid
            WHERE c.city = %s
            order by o.orderNo
            '''
            params = (value)         # SQL문의 실제 파라미터 값의 튜플

        util = DB_Utils()
        rows2 = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows2
    
    def ordersno(self, value):
        sql = '''
            SELECT d.orderLineNo, d.productCode, p.name, d.quantity, d.priceEach, round(d.quantity*d.priceEach, 2) as '상품주문액'
            FROM orders o join orderDetails d on o.orderNo=d.orderNo
            join products p on d.productCode=p.productCode
            WHERE o.orderNo = %s
            order by d.orderLineNo
            '''
        params = (value)         # SQL문의 실제 파라미터 값의 튜플

        util = DB_Utils()
        rows2 = util.queryExecutor(db="classicmodels", sql=sql, params=params)
        return rows2

############################################################################ 주문상세 페이지 

class MainWindow1(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI1()
    def setupUI1(self):

        self.setWindowTitle("주문상세")
        self.setGeometry(0, 0, 1150, 650)
        self.label0 = QLabel("주문 상세 내역:", self)
        self.label = QLabel("주문번호:", self)

        self.Label = QLabel(self)

        
        self.label1 = QLabel("상품개수:", self)

        self.Label1 = QLabel(self)

        
        self.label2 = QLabel("주문액:", self)

        self.Label2 = QLabel(self)

        
        self.tableWidget = QTableWidget(self)   # QTableWidget 객체 생성

        
        self.label3 = QLabel("파일 출력:", self)

        self.radioBtn1 = QRadioButton("CSV", self)

        self.radioBtn1.setChecked(True)
        self.radioBtn2 = QRadioButton("JSON", self)
       
        self.radioBtn3 = QRadioButton("XML", self)

        self.pushButton = QPushButton("저장", self)

        layout1 = QGridLayout()
        layout1.addWidget(self.label0, 0,1)
        layout1.addWidget(self.label, 1,1)
        layout1.addWidget(self.label1, 1,3)
        layout1.addWidget(self.label2, 1,5)
        layout1.addWidget(self.Label, 1,2)
        layout1.addWidget(self.Label1, 1,4)
        layout1.addWidget(self.Label2, 1,6)
        
        layout2 = QGridLayout()
        layout2.addWidget(self.tableWidget, 0, 1)
        
        layout3 = QGridLayout()
        layout3.addWidget(self.label3, 0, 1) 
        layout3.addWidget(self.radioBtn1, 1, 1) 
        layout3.addWidget(self.radioBtn2, 1, 3) 
        layout3.addWidget(self.radioBtn3, 1, 5) 
        layout3.addWidget(self.pushButton, 2, 7) 
        
        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        
        self.setLayout(layout)
        
        
        
############################################################################ 주문 페이지        
        
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):

        # DB 검색문 실행
        query = DB_Queries()
        rows = query.selectPlayerPosition()        # 딕셔너리의 리스트
        rows1 = query.selectCountry()
        rows2 = query.selectCity()
        print(rows)
        print(rows1)
        print(rows2)
        print()
       

        # 윈도우 설정
        self.setWindowTitle("주문 내역")
        self.setGeometry(0, 0, 1150, 650)
        

        # 라벨 설정
        self.label0 = QLabel("주문 검색", self)
        self.label = QLabel("검색된 주문의 개수:", self)
        
        self.Label = QLabel(self)
        
        self.label1 = QLabel("고객:", self)
        
        self.label2 = QLabel("국가:", self)
        
        self.label3 = QLabel("도시:", self)
        

        # 콤보박스 설정
        columnName = list(rows[0].keys())[0]
        self.items = [str(row[columnName]) for row in rows]
        All = ["ALL"]

        self.comboBox = QComboBox(self)
        self.comboBox.addItems(All)
        self.comboBox.addItems(self.items)
        self.comboBox.activated[str].connect(lambda :self.selectedComboItem(self.comboBox))
        
        
        columnName1 = list(rows1[0].keys())[0]
        self.items1 = [str(row[columnName1]) for row in rows1]
        All = ["ALL"]

        self.comboBox1 = QComboBox(self)
        self.comboBox1.addItems(All)
        self.comboBox1.addItems(self.items1)
        self.comboBox1.activated[str].connect(lambda :self.selectedComboItem(self.comboBox1))
        
        
        columnName2 = list(rows2[0].keys())[0]
        self.items2 = [str(row[columnName2]) for row in rows2]
        All = ["ALL"]

        self.comboBox2 = QComboBox(self)
        self.comboBox2.addItems(All)
        self.comboBox2.addItems(self.items2)
        self.comboBox2.activated[str].connect(lambda :self.selectedComboItem(self.comboBox2))
        
        
        # 푸쉬버튼 설정
        self.pushButton = QPushButton("검색", self)
        self.pushButton.clicked.connect(self.pushButton_Clicked)
        
        
        self.pushButton1 = QPushButton("초기화", self)
        self.pushButton1.clicked.connect(self.comboBox_Activated)
        

        # 테이블위젯 설정
        self.tableWidget = QTableWidget(self)   # QTableWidget 객체 생성
        
        
        players = query.selectPlayerUsingPosition('ALL')

        self.Label.setText(str(len(players)))
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(players))
        self.tableWidget.setColumnCount(len(players[0]))
        columnNames = list(players[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(columnNames)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        for rowIDX, player in enumerate(players):                              # player는 딕셔너리임.
            for columnIDX, (k, v) in enumerate(player.items()):
                if v == None:                               # 파이썬이 DB의 널값을 None으로 변환함.
                    continue                                # QTableWidgetItem 객체를 생성하지 않음
                elif isinstance(v, datetime.date):          # QTableWidgetItem 객체 생성
                    item = QTableWidgetItem(v.strftime('%Y-%m-%d'))
                else:
                    item = QTableWidgetItem(str(v))

                self.tableWidget.setItem(rowIDX, columnIDX, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        
        layout1 = QGridLayout()
        layout1.addWidget(self.label0, 0,1)
        layout1.addWidget(self.label, 3,1)
        layout1.addWidget(self.Label, 3,2)
        layout1.addWidget(self.label1, 2,1)
        layout1.addWidget(self.label2, 2,4)
        layout1.addWidget(self.label3, 2,8)
        layout1.addWidget(self.comboBox, 2,2)
        layout1.addWidget(self.comboBox1, 2,5)
        layout1.addWidget(self.comboBox2, 2,9)
        layout1.addWidget(self.pushButton, 2,15)
        layout1.addWidget(self.pushButton1, 3,15)
        
        layout2 = QGridLayout()
        layout2.addWidget(self.tableWidget, 0, 0)
        
        layout = QVBoxLayout()
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        
        self.setLayout(layout)
        
        
        self.tableWidget.cellClicked.connect(self.pushButton1_Clicked)
        
        
    def pushButton1_Clicked(self,row, col):
        self.oo = self.tableWidget.item(row, 0).text()
        query = DB_Queries()
        m = MainWindow1()
        
        players = query.ordersno(self.oo)

        m.Label.setText(self.oo)
        m.tableWidget.clearContents()
        m.tableWidget.setRowCount(len(players))
        m.tableWidget.setColumnCount(len(players[0]))
        columnNames = list(players[0].keys())
        m.tableWidget.setHorizontalHeaderLabels(columnNames)
        m.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        for rowIDX, player in enumerate(players):                              # player는 딕셔너리임.
            for columnIDX, (k, v) in enumerate(player.items()):
                if v == None:                               # 파이썬이 DB의 널값을 None으로 변환함.
                    continue                                # QTableWidgetItem 객체를 생성하지 않음
                elif isinstance(v, datetime.date):          # QTableWidgetItem 객체 생성
                    item = QTableWidgetItem(v.strftime('%Y-%m-%d'))
                else:
                    item = QTableWidgetItem(str(v))

                m.tableWidget.setItem(rowIDX, columnIDX, item)

        m.tableWidget.resizeColumnsToContents()
        m.tableWidget.resizeRowsToContents()
        rowcount1 = m.tableWidget.rowCount()
        m.Label1.setText(str(rowcount1))
        
        j=0
        for i in range(rowcount1):
            j+=float(m.tableWidget.item(i, 5).text())
        m.Label2.setText(str(round(j,2)))
        
        
        def write1():
            if m.radioBtn1.isChecked() == True:
                # CSV 화일을 쓰기 모드로 생성
                with open(f'{self.oo}.csv', 'w', encoding='utf-8', newline='') as f:
                    wr = csv.writer(f)
                    # 테이블 헤더를 출력
                    columnNames = list(players[0].keys())
                    wr.writerow(columnNames)
                    # 테이블 내용을 출력
                    for row in players: # row는 딕셔너리
                        pp1 = list(row.values()) # player는 리스트
                        wr.writerow(pp1)
            if m.radioBtn2.isChecked() == True:
                for i in range(len(players)):
                    a = players[i]["상품주문액"]
                    players[i]["상품주문액"]=float(a)
                    b = players[i]["priceEach"]
                    players[i]["priceEach"]=float(b)           
                newDict = dict(Orders = players)
                with open(f'{self.oo}.json', 'w', encoding='utf-8') as f:
                    json.dump(newDict, f, ensure_ascii=False)     
            if m.radioBtn3.isChecked() == True:
                for i in range(len(players)):
                    a = players[i]["상품주문액"]
                    players[i]["상품주문액"]=float(a)
                    b = players[i]["priceEach"]
                    players[i]["priceEach"]=float(b)
                newDict = dict(Orders = players)
                tableName = list(newDict.keys())[0]
                tableRows = list(newDict.values())[0]
                rootElement = ET.Element('TABLE')
                rootElement.attrib['name'] = tableName
                for row in tableRows:
                    rowElement = ET.Element('ROW')
                    rootElement.append(rowElement)
                    for columnName in list(row.keys()):
                        if row[columnName] == None: 
                            rowElement.attrib[columnName] = ''
                        elif type(row[columnName]) == int or type(row[columnName]) == float: 
                            rowElement.attrib[columnName] = str(row[columnName])
                        else:
                            rowElement.attrib[columnName] = row[columnName]
                ET.ElementTree(rootElement).write(f'{self.oo}.xml', encoding='utf-8', 
                                xml_declaration=True)

            
        m.pushButton.clicked.connect(write1)
            

        
        m.show()
        try:
            sys.exit(m.exec_())
        except:
            pass
        

    def selectedComboItem(self,text):
    
        self.aa=text.currentText()
    
    def comboBox_Activated(self):
        
        query = DB_Queries()

        players = query.selectPlayerUsingPosition('ALL')

        self.Label.setText(str(len(players)))
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(len(players))
        self.tableWidget.setColumnCount(len(players[0]))
        columnNames = list(players[0].keys())
        self.tableWidget.setHorizontalHeaderLabels(columnNames)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        for rowIDX, player in enumerate(players):                              # player는 딕셔너리임.
            for columnIDX, (k, v) in enumerate(player.items()):
                if v == None:                               # 파이썬이 DB의 널값을 None으로 변환함.
                    continue                                # QTableWidgetItem 객체를 생성하지 않음
                elif isinstance(v, datetime.date):          # QTableWidgetItem 객체 생성
                    item = QTableWidgetItem(v.strftime('%Y-%m-%d'))
                else:
                    item = QTableWidgetItem(str(v))

                self.tableWidget.setItem(rowIDX, columnIDX, item)

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
    
    def pushButton_Clicked(self):

        # DB 검색문 실행
        query = DB_Queries()
        
        if self.aa == "ALL":
            players = query.selectPlayerUsingPosition(self.aa)
        elif self.aa in self.items:    
            players = query.selectPlayerUsingPosition(self.aa)
        elif self.aa in self.items1: 
            players = query.selectUsingCountry(self.aa)
        elif self.aa in self.items2: 
            players = query.selectUsingCity(self.aa)

        try:
            self.Label.setText(str(len(players)))
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(len(players))
            self.tableWidget.setColumnCount(len(players[0]))
            columnNames = list(players[0].keys())
            self.tableWidget.setHorizontalHeaderLabels(columnNames)
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

            for rowIDX, player in enumerate(players):                              # player는 딕셔너리임.
                for columnIDX, (k, v) in enumerate(player.items()):
                    if v == None:                               # 파이썬이 DB의 널값을 None으로 변환함.
                        continue                                # QTableWidgetItem 객체를 생성하지 않음
                    elif isinstance(v, datetime.date):          # QTableWidgetItem 객체 생성
                        item = QTableWidgetItem(v.strftime('%Y-%m-%d'))
                    else:
                        item = QTableWidgetItem(str(v))

                    self.tableWidget.setItem(rowIDX, columnIDX, item)
        except:
            pass

#########################################

def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

main()