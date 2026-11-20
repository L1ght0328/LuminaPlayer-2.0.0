class Settings:
    DEFAULTS={"theme_mode":"dark","palette":"Lumina","custom_accent":"","volume":"70","shuffle":"0",
              "repeat":"off","reduce_motion":"0","pause_audio_on_video":"1","window_width":"1366",
              "window_height":"768","window_mode":"normal","last_track":"","last_position":"0"}
    def __init__(self,db):
        self.db=db
        for k,v in self.DEFAULTS.items():
            if db.setting(k) is None: db.set_setting(k,v)
    def get(self,k,default=None):
        v=self.db.setting(k,self.DEFAULTS.get(k,default))
        if v in ("0","1"): return v=="1"
        return v
    def set(self,k,v):
        if isinstance(v,bool): v="1" if v else "0"
        self.db.set_setting(k,v)
