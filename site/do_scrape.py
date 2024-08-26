import pickle
import datetime
import json
import traceback
import logging
from datetime import date, time
from trawlers import cgttv, SidRoth, csafeTV, tct, cLLbn, emmatv, cwgntv, ckchf, njeta, c3abnAll, cwn, ccstv, cetv, cLFT, cTLN, cSLSTV, ckcs_end, cWHTv, c3ABNF, ccbn, csat7A, csat7T, csat7P, csat7K, ccyc, caft, cin, ctw, cicfn, cmnn, ctv45, cgeb, cgodtv, cflnz, cds, cglc, crt, chtv, cptv, cmis, cnm, chc, cbvov, charvesttv, cffe, cad, cWACX, c3abnRussian, csonliveTV, cnh, ckcse, cft, jbs, cabn
import sys

# Set recursion limit and initialize recursion counter
sys.setrecursionlimit(50000)
print("Recursion limit:", sys.getrecursionlimit())

# Initialize global counter for tracking recursion depth
recursion_counter = 0

logging.basicConfig(level=logging.INFO)

def add_ordinal(n):
    return str(n) + ("th" if 4 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))

days = []
days_js = []

def update_days():
    today = datetime.date.today()

    for d in range(7):
        days.append(today + datetime.timedelta(days=d))

    for d in days:
        human = add_ordinal(d.day)
        human += d.strftime(" %b")

        entry = {
            "date": d.strftime("%Y-%m-%d"),
            "day": d.strftime("%A"),
            "human_date": human}
        days_js.append(entry)

schedules = {}

def recursive_function_wrapper(func, *args, **kwargs):
    global recursion_counter
    recursion_counter += 1
    return func(*args, **kwargs)

def update_schedules():
    global schedules

    schedule_data = {
        1: cgttv.TrawlerGospelTruthTV,  # A
        2: cmis.TrawlerMyersInfoSys,
        3: ccbn.TrawlerCBN,
        # 4 M
        5: ccyc.TrawlerCYC,
        6: cTLN.TrawlerTotalLN,
        # 7 M
        8: ckcs_end.TrawlerKCSETVLifeEnd,
        9: cin.TrawlerImpactNetwork,
        10: caft.TrawlerAmazingFactsTV,
        11: ctw.TrawlerTheWalk,
        12: cicfn.TrawlerICFN,
        13: cmnn.TrawlerMNN,
        14: c3abnRussian.TrawlercRussian,
        15: csat7P.TrawlerSAT_7_PARS,
        16: csat7T.TrawlerSAT_7_TURK,
        17: csat7A.TrawlerSAT_7_ARABIC,
        18: ctv45.TrawlerTV45,
        # 19 M
        20: cgeb.TrawlerGEB,
        21: csonliveTV.TrawlercsonliveTV,
        22: cWHTv.TrawlerWorldHarvestTV,
        23: cLFT.TrawlerLivingFTV,  # F
        24: cflnz.TrawlerFirstLight,
        25: cds.TrawlerDayStar,
        26: c3abnAll.Trawlerc3abnLll,
        27: cSLSTV.TrawlerSmartLSTV,
        28: tct.Trawlertct,
        # 29 M
        30: cglc.TrawlerGLC,
        31: emmatv.TrawlerEmmanuelTV,
        32: cnh.TrawlerNewHope,
        # 33 M
        # 34 M
        35: c3ABNF.Trawler3ABNF,
        36: c3abnAll.Trawlerc3abnLll,
        37: c3abnAll.Trawlerc3abnLll,
        # 38 M
        39: cWACX.Trawlerwacx,      # F
        40: cgodtv.TrawlerGodTV,
        41: cgodtv.TrawlerGodTV,
        42: cgodtv.TrawlerGodTV,
        43: cgodtv.TrawlerGodTV,
        44: cgodtv.TrawlerGodTV,
        45: cetv.TrawlerCBNFamily,
        46: csafeTV.TrawlerSafeTv,
        47: cLLbn.TrawlerCLLBN,
        48: cLLbn.TrawlerCLLBN,
        49: cLLbn.TrawlerCLLBN,
        # 50 M
        51: c3abnAll.Trawlerc3abnLll,
        52: cmis.TrawlerMyersInfoSys,
        53: cwn.TrawlerWorldNetwork,
        54: chtv.TrawlerHopeTV,
        55: ccstv.TrawlerCornerstone,
        56: cLLbn.TrawlerCLLBN,
        57: ckchf.Trawlerckchf,
        # 58 M
        59: cabn.TrawlerABN,
        60: SidRoth.TrawlerSidRoth,
        61: cmis.TrawlerMyersInfoSys,
        62: cptv.TrawlerPressTV,
        63: njeta.TrawlerNjetaTV,
        64: jbs.TrawlerJewishB,
        65: cwgntv.TrawlerWGNchicago,
        66: crt.TrawlerRT,
        67: cnm.TrawlerNewsMax,
        68: cft.TrawlerFamilyTV,
        # 69 M
        70: c3abnAll.Trawlerc3abnLll,
        71: c3abnAll.Trawlerc3abnLll,
        72: tct.Trawlertct,
        73: chc.TrawlerHisChannel,
        # 74 M - to be removed
        75: cbvov.TrawlerBVOV,
        # 76 M
        77: charvesttv.TrawlerHarvestTV,
        78: csat7K.TrawlerSat7Kids,
        79: cffe.TrawlerFFE,
        80: cad.Trawlercad,
        81: ckcse.TrawlerKCSETVLife,
    }

    extra_args = {
        2: 'nrb',
        26: 'main',
        28: 'hd',
        36: 'lat',
        37: 'int',
        40: 'as',
        41: 'af',
        42: 'au',
        43: 'uk',
        44: 'us',
        47: 'llbnlatino',
        48: 'llbnsouthasia',
        49: 'llbnarabic',
        51: 'kids',
        52: 'gbntv',
        56: 'hiswordhd',
        61: 'jltv',
        70: 'dare',
        71: 'proc',
        72: 'kids'
    }

    for channel_number in schedule_data:
        sd = {}
        try:
            logging.info("Running [{}] {}".format(channel_number, schedule_data[channel_number].__name__))
            if channel_number in extra_args:
                sd = {
                    str(channel_number): recursive_function_wrapper(
                        schedule_data[channel_number].get_info_for_days,
                        days, extra_args[channel_number]
                    )
                }
            else:
                sd ={
                    str(channel_number): recursive_function_wrapper(
                        schedule_data[channel_number].get_info_for_days,
                        days
                    )
                }
        except Exception as e:
            sd = []
            logging.error("Error occurred in scraper {}: {}".format(schedule_data[channel_number].__name__, e))
            traceback.print_exc()
            # pass
        finally:
            schedules.update(sd)

update_days()
update_schedules()

day_data = {"days": days, "days_js": days_js}

with open('./cache/days.pickle', 'wb+') as days_dump_handle:
    pickle.dump(day_data, days_dump_handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./cache/schedule.pickle', 'wb+') as sched_dump_handle:
    pickle.dump(schedules, sched_dump_handle, protocol=pickle.HIGHEST_PROTOCOL)

# After running the code, if a RecursionError occurs, the following will print the recursion depth.
# try:
#     update_schedules()
# except RecursionError:
#     print(f"Recursion depth reached: {recursion_counter}")
