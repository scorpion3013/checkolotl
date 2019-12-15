import checkolotl.welcome as welcome
import checkolotl.version as version
import checkolotl.proxy as proxychecker
import checkolotl.utils.input_thread as command_handler
import checkolotl.check as checker
import checkolotl.saver as saver
import checkolotl.timeout as exit_timer
from checkolotl.events import start as start_event, end as end_event


exit_timer.start()
welcome.message()
version.update_check()
command_handler.start()
start_event.start()
proxychecker.start()
saver.start()
checker.start()
end_event.start()
