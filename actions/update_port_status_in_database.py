from st2actions.runners.pythonrunner import Action
from lib import actions
import pymysql.cursors

class RpvlanUpdateMacAuthFailureDatabaseAction(actions.SessionAction):
  def __init__(self,config):
     super(RpvlanUpdateMacAuthFailureDatabaseAction, self).__init__(config)

  def run(self, timestamp, switch_name, ip, ap_name, port, action, mac):

     if action=='add':
         self.process_add_port(timestamp, switch_name, ip, ap_name, port, mac)

     if action=='remove':
         self.process_remove_port(timestamp, switch_name, ip, ap_name, port, mac)

     # TODO: Report errors like database failure!
     return (True)

  def process_add_port(self, timestamp, switch_name, ip, ap_name, port, mac):
        connection = pymysql.connect(
             host=self._db_addr, 
             user=self._db_user,      
             passwd=self._db_pass,  
             db=self._db_name)

        cursor = connection.cursor()
        sql = "update authorized set switch_name='%s', ip='%s', port='%s', timestamp='%s' where mac='%s'" % (switch_name, ip, port, timestamp, mac)
        cursor.execute(sql)
        connection.commit()
        connection.close()

  def process_remove_port(self, timestamp, switch_name, ip, ap_name, port, mac):
        connection = pymysql.connect(
             host=self._db_addr, 
             user=self._db_user,      
             passwd=self._db_pass,  
             db=self._db_name)
        
        cursor = connection.cursor()
        sql = "update authorized set switch_name='NULL', ip='NULL', port='NULL', timestamp='NULL' where ip='%s' and mac='%s'" % (ip, mac)
        cursor.execute(sql)

	sql = "delete from failures where port='%s' and ip='%s'" % (port, ip)
        cursor.execute(sql)
        cursor.close()
        connection.commit()
        connection.close()

