# Script de Simulação de Estados e Validação do Unifilar SCADA
# EcoStruxure Power SCADA Operation

class Breaker:
    def __init__(self, name, status="OPEN", voltage=0.0):
        self.name = name
        self.status = status  # "CLOSED" or "OPEN"
        self.voltage = voltage

class SCADAUnifilarSystem:
    def __init__(self):
        # Componentes mapeados a partir da tela SCADA
        self.trf_a = Breaker("TRF A", "CLOSED", 480.0)
        self.trf_b = Breaker("TRF B", "CLOSED", 480.0)
        self.gen_a = Breaker("Gen A Breaker", "OPEN", 0.0)
        self.gen_b = Breaker("Gen B Breaker", "OPEN", 0.0)
        self.ax_cpl = Breaker("AX CPL", "OPEN", 0.0)
        self.bx_cpl = Breaker("BX CPL", "OPEN", 0.0)
        self.ab_cpl = Breaker("AB CPL (Interlocked)", "OPEN", 0.0)

    def evaluate_bus_states(self):
        bus_a_energized = (self.trf_a.status == "CLOSED") or (self.ax_cpl.status == "CLOSED" and self.gen_a.status == "CLOSED")
        bus_b_energized = (self.trf_b.status == "CLOSED") or (self.bx_cpl.status == "CLOSED" and self.gen_b.status == "CLOSED")
        
        interlock_active = (self.trf_a.status == "CLOSED") and (self.trf_b.status == "CLOSED")
        
        return {
            "Bus_A_Status": "ENERGIZED" if bus_a_energized else "DEENERGIZED",
            "Bus_B_Status": "ENERGIZED" if bus_b_energized else "DEENERGIZED",
            "AB_CPL_Interlocked": interlock_active
        }

if __name__ == '__main__':
    scada = SCADAUnifilarSystem()
    print("=== ESTADO ATUAL DO SISTEMA SCADA ===")
    print(scada.evaluate_bus_states())
