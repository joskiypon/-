__version__ = (2,0,0)
# meta developer: @Not_Toxa (лошик привет)

from .. import loader, utils
import logging
import re
from typing import Optional, Union, Tuple

logger = logging.getLogger(__name__)
pattern = re.compile("\d+-\d+")

@loader.tds
class BioCounter(loader.Module):
    """Модуль для подсчёта стоимостей в ирисе"""
    strings = {
        "name": "BioCounter"
    }
    
    async def калкcmd(self, m) -> None:
        """Команда для подсчёта"""
        args = utils.get_args(m)
        ifs = await normal_args(args)
        if ifs is True:
            await utils.answer(m, await resulter(args))
        elif isinstance(ifs, str):
            await utils.answer(m, ifs)
        
async def resulter(args) -> str:
    factor = await action_factor(args[0])
    if pattern.match(args[1]):
        price = sum(
                [await counter(
                    lvl, factor[0]
                ) for lvl in range(
                    *list(map(lambda x: int(x)+1, args[1].split("-")))
                )]
            )
        return "❓ Для повышения навыка «{0}» с {1} до {2} потребуется {3:,}{4}🧬".format(
            factor[1], *args[1].split("-"), price, ("k" if price >= 1000 else "")
        ).replace(","," ")
    else:
        price = await counter(
                int(args[1]), factor[0]
            )
        return "❓ Для повышения навыка «{0}» до {1} требуется {2:,}{3} 🧬".format(
            factor[1], args[1], price, ("k" if price >= 1000 else "")
       ).replace(",", " ")

async def normal_args(args) -> Union[bool, str]:
    if not len(args) == 2:
        return "<b>Указано не допустимое количество аргументов</b>"
    elif await action_factor(args[0]) is None:
        return "<b>Данная характеристика отсутсвует</b>"
    elif not args[1].isdigit():
        if pattern.match(args[1]):
            return True
        else:
            return "<b>Второй аргумент является не допустимым значением</b>"
    else:
        return True

async def action_factor(
    factor: str
    ) -> Optional[
        Tuple[Union[int, float], str]
        ]:
    if factor in (
        'заразность', 
        'зз', 
        ): return (2.5, "заразность", )
    elif factor in (
        "квалификация",
        "учёные",
        "ученые",
        "квал",
        ): return (2.6, "квалификация", )
    elif factor in (
        "патогены",
        "патоген"
        "пат",
        "паты",
        ): return (2, "патогены", )
    elif factor in (
        "иммунитет",
        "имун",
        ): return (2.45, "иммунитет", )
    elif factor in (
        "летальность",
        "летал",
        "леталка",
        ): return (1.95, "летальность", )
    elif factor in (
        "безопасность",
        "сб",
        ): return (2.1, "безопасность", )

async def counter(lvl: int, factor: Union[int, float]) -> int:
    return int(lvl**factor)