from fastapi import APIRouter, Depends, Query

from app.db.enums import CoursePair
from app.depends.get_course_pair import get_course_pair
from app.models.exchange_rate_pare import ExchangeRateModel
from app.repositories.exchange_rate import ExchangeRetaRepository
from app.repositories.providers import provide_exchange_rate_repository_stub

exchange_rate_router = APIRouter(tags=["Exchange Rate"], prefix="/exchange_rate/api/v1")


@exchange_rate_router.get("/courses", response_model=list[ExchangeRateModel.GET])
async def get_courses(
        course_rate_pare: CoursePair | None = Depends(get_course_pair),
        exchange_rate_repository: ExchangeRetaRepository = Depends(provide_exchange_rate_repository_stub),
):
    """
    Получить курсы обмена валют.

    Возможные варианты обмена:
    - BTCUSDT: Обмен Bitcoin на Tether (USDT)
    - BTCRUB: Обмен Bitcoin на российский рубль (RUB)
    - ETHUSDT: Обмен Ethereum на Tether (USDT)
    - ETHRUB: Обмен Ethereum на российский рубль (RUB)
    - USDTTRCUSDT: Обмен Tether на TrueUSD (USDT)
    - USDTTRCRUB: Обмен Tether на TrueUSD (RUB)
    - USDTERCUSDT: Обмен TrueUSD на Tether (USDT)
    - USDTERCRUB: Обмен TrueUSD на Tether (RUB)
    """
    return await exchange_rate_repository.find_all(course_rate_pare)
