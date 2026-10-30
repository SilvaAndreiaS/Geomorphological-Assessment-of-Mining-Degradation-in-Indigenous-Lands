# PLANO DE TESTES E HOMOLOGAÇÃO: SISTEMA SCADA / UNIFILAR ELÉTRICO
**Sistema:** EcoStruxure Power SCADA Operation (Schneider Electric)  
**Tabela / Unifilar:** Main MV SwitchBoard (Média e Baixa Tensão)  
**Versão:** 1.0  

---

## 1. Visão Geral do Sistema Visualizado

O diagrama unifilar apresenta a distribuição elétrica dividida em duas vias principais da concessionária (**Utility Switchgear A** e **Utility Switchgear B**) e um barramento de emergência alimentado por geradores (**Generator Switchboard - Gen A e Gen B**).

### Componentes Principais Mapeados:
1. **Fontes Principais:**
   - **Utility A:** Entradas em $12.47	ext{ kV}$ passando por relé Sepam A, transformador Trans A e disjuntor TRF A.
   - **Utility B:** Entradas em $12.48	ext{ kV}$ passando por relé Sepam B, transformador Trans B e disjuntor TRF B.
2. **Fontes de Emergência:**
   - **Gen A Breaker & Gen B Breaker:** Alimentam o barramento intermediário **Bus X**.
   - **AX CPL / BX CPL:** Disjuntores de acoplamento do barramento de geradores para os barramentos de carga.
3. **Barramentos e Acoplamento de Carga:**
   - **Bus A ($480	ext{ V}$):** Alimenta Mech Dist A, Mech UPS Board A, IT UPS Input Board A, Aux Supplies Board A.
   - **Bus B ($480	ext{ V}$):** Alimenta Mech Dist B, Mech UPS Board B, IT UPS Input Board B, Aux Supplies Board B.
   - **AB CPL (Tie-Breaker):** Interlock entre Bus A e Bus B (Atualmente **Interlocked / Aberto**).

---

## 2. Roteiro e Procedimentos de Teste (Passo a Passo)

### Teste 1: Operação Normal na Rede da Concessionária (Concessionária A e B Ativas)
- **Objetivo:** Verificar se a carga dos barramentos A e B é suprida independentemente pelas concessionárias A e B.
- **Procedimento:**
  1. Fechar disjuntor **TRF A** ($480	ext{ V}$).
  2. Fechar disjuntor **TRF B** ($480	ext{ V}$).
  3. Manter **Gen A**, **Gen B**, **AX CPL**, **BX CPL** e **AB CPL** ABERTOS.
- **Resultado Esperado:** 
  - Bus A energizado em $480	ext{ V}$ via Utility A.
  - Bus B energizado em $480	ext{ V}$ via Utility B.
  - Sinalização verde/vermelha e medições elétricas refletindo estado correto na IHM SCADA.

---

### Teste 2: Falha na Concessionária A e Transição para Geradores (Transferência de Carga)
- **Objetivo:** Validar a lógica de transferência automática de carga em caso de blackout na entrada A.
- **Procedimento:**
  1. Simular falha de tensão no **Utility Switchgear A** ($12.47	ext{ kV}$).
  2. Verificar disparo e abertura do disjuntor **TRF A**.
  3. Confirmar comando automático de partida do gerador **Gen A**.
  4. Após estabilização da tensão/frequência, verificar fechamento dos disjuntores **Gen A Breaker** e **AX CPL**.
- **Resultado Esperado:**
  - Bus A passa a ser alimentado pelo barramento **Bus X** ($480	ext{ V}$).
  - Alarme de "Falha de Concessionária A" registrado na lista de Alarmes/Eventos.

---

### Teste 3: Intertravamento e Acoplamento de Barramentos (AB CPL Interlock)
- **Objetivo:** Garantir a proteção contra o paralelismo não sincronizado entre Bus A e Bus B.
- **Procedimento:**
  1. Com **TRF A** fechado e **TRF B** fechado, tentar comando manual de fechamento do disjuntor **AB CPL**.
- **Resultado Esperado:**
  - O sistema SCADA deve bloquear o comando indicando a condição **Interlocked**.
  - Impede curto-circuito e paralelismo indevido entre fontes não sincronizadas.

---

## 3. Matriz de Cobertura de Testes Automáticos (Casos de Teste)

| ID | Cenário | Condição de Entrada | Ação Esperada | Status do Teste |
|---|---|---|---|---|
| **TC-01** | Operação Normal | Utility A & B $12.47	ext{ kV}$ Ok | TRF A e TRF B fechados; Bus A e B $480	ext{ V}$ | PASS |
| **TC-02** | Blackout Concessionária A | Falha de sinal em Utility A | Partida de Gen A; Fechamento AX CPL | PASS |
| **TC-03** | Blackout Concessionária B | Falha de sinal em Utility B | Partida de Gen B; Fechamento BX CPL | PASS |
| **TC-04** | Bloqueio de Intertravamento | Fechar AB CPL com TRF A e B ON | Rejeição de comando (Interlocked) | PASS |
| **TC-05** | Reset de Sobrecarga/Falha | Trip de proteção Sepam 50/51 | Geração de Alerta Crítico e log | PASS |
