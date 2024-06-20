# MQTT Signals Aggregator 

Sygnały są w formacie JSON:
```json
{
  time:"2024-01-01T00:00:00Z",
  value:2137.12,
  unit: "V"
}
```
Do programu przygotowano w ramach testu także prosty generator sygnałów MQTT. 
Cały projekt jest możliwy do uruchomienia w dockerze. 

## Ograniczenia
W momencie kiedy sygnały są wysyłane co sekundę, i gdy N jest ustawione na bardzo niską wartość, program agreguje więcej pomiarów. 

