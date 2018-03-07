import pymysql


class OperateMysql(object):
    def __init__(self, exec_sql):
        try:
            # 打开数据库连接
            self.conn = pymysql.connect(host="192.168.0.104", port=3306, user="yhc", passwd="mymysql", db="netdata", charset='utf8')
            # 创建游标 游标设置为字典类型
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            self.sql = exec_sql
        except Exception as e:
            print("Database connection failure.error：%s"% e)

    def executeSql(self):
        r = self.cursor.execute(self.sql, self.param)
        self.conn.commit()
        return r

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":

    sql = 'select * from 36ke_news'
    operate = OperateMysql(sql)
    result = operate.executeSql()
    if result > 0:
        for index in operate.cursor:
            print(index['ke_item'])