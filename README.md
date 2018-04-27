# Hekar
Tries to get active region of a flare using hek's api.

**_NOTE_**: This is a very specific library, it just tries to compare data gotten from RHESSI, if that's not what you need, don't use it. But, feel free to make the changes you need.

```python
from hekar import HEK

event_stattime = "2002-04-09T12:45:00"
event_endtime = "2002-04-09T13:05:00"

hek = HEK(event_starttime, event_endtime)
active_region = hek.get_active_region()
```
