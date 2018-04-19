# Hekar
Tries to get active region of a flare using hek's api

```python
from hekar import HEK

event_stattime = "2002-04-09T12:45:00"
event_endtime = "2002-04-09T13:05:00"

hek = HEK(event_starttime, event_endtime)
active_region = hek.get_active_region()
```
