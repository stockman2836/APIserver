from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Представление состояния системы безопасности
class SystemStatus(BaseModel):
    alarmActive: bool
    sensorsBlocked: bool

# Глобальное состояние системы безопасности
global_status = {"alarmActive": False, "sensorsBlocked": False}

@app.post("/toggle-system/")
async def toggle_system():
    # Переключаем состояния системы
    global_status["alarmActive"] = not global_status["alarmActive"]
    global_status["sensorsBlocked"] = not global_status["sensorsBlocked"]
    return {"message": "System toggled", "status": global_status}

@app.post("/disable-alarm/")
async def disable_alarm():
    # Отключаем сигнализацию, если она активна
    if global_status["alarmActive"]:
        global_status["alarmActive"] = False
        # Активируем датчики, если они были заблокированы
        global_status["sensorsBlocked"] = True
        return {"message": "Alarm disabled", "status": global_status}
    # Если сигнализация уже выключена, изменений не происходит
    return {"message": "Alarm is already disabled", "status": global_status}

@app.post("/update/")
async def update_status(status: SystemStatus):
    # Обновляем статус системы безопасности
    global_status.update(status.dict())
    return {"status": global_status}

@app.get("/status/")
async def get_status():
    # Получаем текущий статус системы безопасности
    return global_status
