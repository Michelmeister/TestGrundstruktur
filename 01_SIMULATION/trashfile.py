

    def strategy_depth_discharge_protection(self):
        'Entladegrenze physikalisch -> SoC = 5%'

        if BSS.E_bat_device <= (0.049 * BSS.E_bat_max):

            if BSS.E_bat_device <= (0.043 * BSS.E_bat_max):
                p_bat_v = -25

            elif BSS.E_bat_device >= (0.048 * BSS.E_bat_max):
                p_bat_v = 0
            else:
                pass






            'Erhaltungsladung ab SoC = 4,5%'
            self.P_bat_v = -25 - self.P_pv_v # Alle WE laden mit 25 W um SoC = 4,5% aufrecht zu erhalten
            self.P_pv_usage = self.P_pv_v
            self.P_pv_feedin = 0
            self.dE_v = (-self.P_bat_v/3600) * BSS.efficiency
            self.P_Netz_v = self.P_load_v + self.P_Wallbox - self.P_bat_v
            self.E_bat_v = self.E_bat_v + self.dE_v





        elif P_pv_sum >= P_load_sum + P_Wallbox_sum:
            self.E_bat_v = self.E_bat_v + self.dE_v
            self.P_pv_usage = self.P_pv_v
            self.P_pv_feedin = 0
            self.P_bat_v = round(self.P_load_v + self.P_Wallbox - self.P_pv_v,2)
            self.P_Netz_v = self.P_load_v + self.P_Wallbox - self.P_pv_v - self.P_bat_v

        elif P_pv_sum < P_load_sum + P_Wallbox_sum:
            self.P_bat_v = 0
            self.P_pv_usage = self.P_pv_v
            self.P_pv_feedin = 0
            self.P_Netz_v = self.P_load_v + self.P_Wallbox - self.P_pv_v
