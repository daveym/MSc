require 'hl7util'
require 'stringutil'
require 'dateparse'
require 'node'

-- Use the full path to the DB
SQLITE_DB='/users/daveymcglade/Dropbox/MSc/Msc.Project/Code/avail/hl7-combined.db' 

conn = db.connect{api=db.SQLITE, name=SQLITE_DB}

function main(Data)

   local T = MapData(Data)
   
   if T then
      -- Live = true commits db writes whilst in the editor.
      conn:merge{data=T, live=true}
   end 
  
end

function MapData(Data)
   
   local Msg,Name = hl7.parse{vmd='HL7toDB0.3.vmd', data=Data}
   local Out      = db.tables{vmd='HL7toDB0.3.vmd', name=Name}
   local T = os.time()
   
   -- SQlite doesnt have a date datatype. Store dates as ISO8601 string format
   -- YYYY-MM-DD HH:MM:SS.SSS. Query using select * from messages where 
   -- QueueTime  > '2017-07-18T19:56:49' and QueueTime < '2017-07-18T19:56:55'
   
   Out.messages[1].QueueTime = os.date("%Y-%m-%d %H:%M:%S", T)
   
   local TimeString = Msg.MSH[7][1]:nodeValue()
   local MsgTime = dateparse.parse(TimeString)
   
   Out.messages[1].MSGDATETIME = os.date("%Y-%m-%d %H:%M:%S", MsgTime)
   Out.messages[1].MSGCTRLID = Msg.MSH.MessageControlID
   Out.messages[1].MSGTYPE = Msg.MSH[9][3]
   Out.messages[1].PATIENTID = Msg.PID[3][1][1]
   Out.messages[1].FIRSTNAME = Msg.PID[5][1][2]:nodeValue():capitalize()
   Out.messages[1].LASTNAME = Msg.PID[5][1][1][1]:nodeValue():capitalize()
	Out.messages[1].BIRTHDATE =  Msg.PID[7][1]
   
   return Out
   
end