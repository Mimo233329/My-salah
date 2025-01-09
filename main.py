from datetime import date
from pyIslam.praytimes import (
    PrayerConf,
    Prayer,
    LIST_FAJR_ISHA_METHODS,
)
from pyIslam.hijri import HijriDate
import flet
from flet import *

def tz(t):
    return f"GMT{t}" if t < 0 else f"GMT+{t}"

def main(page: flet.Page):
    page.title = "My Salah"
    page.window.width = 390
    page.window.height = 740
    page.window_title_bar_hidden = True
    page.bgcolor = "blue"
    page.scroll = "auto"

    dt = date.today()
    ar = ("Shafii", "Maliki", "Hambali", "Hanafi")

    # City selection
    tx = Text("City:", color="black", size=30, font_family="Constantia")
    ci = TextField(
        prefix_icon=icons.SEARCH,
        helper_text="ex:Cairo",
        hint_text="City name",
        color="black",
    )

    # Dropdowns for methods
    txt = Text("Calculation methods:", color="black", size=30, font_family="Constantia")
    dd = Dropdown(
        helper_text="Choose calculation method",
        color="green",
        options=[dropdown.Option(f"{method.id}: {' | '.join(method.organizations)}") for method in LIST_FAJR_ISHA_METHODS],
    )
    
    madhab_dropdown = Dropdown(
        helper_text="Choose Asr Madhab",
        color="green",
        options=[dropdown.Option(madhab) for madhab in ar],
    )

    output = Text("Output:", color="black", size=30, font_family="Constantia")
    out = Text(value="", color="black", size=20)

    def calculate_prayer_times(e):
        city_name = ci.value.lower()
        city_info = city_data.get(city_name, city_data["cairo"])  # Default to cairo
        longitude, latitude, timezone = city_info["longitude"], city_info["latitude"], city_info["timezone"]

        # Extract method ID and madhab
        fajr_isha_method = int(dd.value.split(":")[0]) if dd.value else 1
        asr_fiqh = ar.index(madhab_dropdown.value) + 1 if madhab_dropdown.value else 1

        # Prayer configuration
        pconf = PrayerConf(longitude, latitude, timezone, fajr_isha_method, asr_fiqh)
        pt = Prayer(pconf, dt)
        hijri = HijriDate.today()

        # Display prayer times
        out.value = (
            f"Timezone: {tz(timezone)}\n"
            f"Fajr and Ishaa reference: {LIST_FAJR_ISHA_METHODS[fajr_isha_method - 1].organizations[0]}\n"
            f"\nPrayer times for: {hijri.format(2)} ({dt})\n"
            f"Fajr      : {pt.fajr_time()}\n"
            f"Sherook   : {pt.sherook_time()}\n"
            f"Dohr      : {pt.dohr_time()}\n"
            f"Asr       : {pt.asr_time()}\n"
            f"Maghreb   : {pt.maghreb_time()}\n"
            f"Ishaa     : {pt.ishaa_time()}\n"
            f"1st third : {pt.second_third_of_night()}\n"
            f"Midnight  : {pt.midnight()}\n"
            f"Qiyam     : {pt.last_third_of_night()}"
        )
        page.update()

    calc_button = ElevatedButton("Calculate", on_click=calculate_prayer_times)

    # Add components to the page
    page.add(
        tx,
        ci,
        txt,
        dd,
        madhab_dropdown,
        calc_button,
        output,
        out,
    )

# City data
city_data = {
    "cairo": {"longitude": 31.2357, "latitude": 30.0444, "timezone": 2},
    "alexandria": {"longitude": 29.9553, "latitude": 31.2001, "timezone": 2},
    "giza": {"longitude": 31.2109, "latitude": 30.0131, "timezone": 2},
    "shubra el kheima": {"longitude": 31.2422, "latitude": 30.1255, "timezone": 2},
    "port said": {"longitude": 32.2841, "latitude": 31.2653, "timezone": 2},
    "suez": {"longitude": 32.5482, "latitude": 29.9668, "timezone": 2},
    "luxor": {"longitude": 32.6396, "latitude": 25.6872, "timezone": 2},
    "aswan": {"longitude": 32.8773, "latitude": 24.0889, "timezone": 2},
    "mansoura": {"longitude": 31.3775, "latitude": 31.0411, "timezone": 2},
    "zagazig": {"longitude": 31.5020, "latitude": 30.5877, "timezone": 2},
    "faiyum": {"longitude": 30.8418, "latitude": 29.3082, "timezone": 2},
    "damietta": {"longitude": 31.8123, "latitude": 31.4165, "timezone": 2},
    "ismailia": {"longitude": 32.2743, "latitude": 30.5965, "timezone": 2},
    "asyut": {"longitude": 31.1711, "latitude": 27.1809, "timezone": 2},
    "minya": {"longitude": 30.7440, "latitude": 28.0936, "timezone": 2},
    "bani suef": {"longitude": 31.0761, "latitude": 29.0661, "timezone": 2},
    "qena": {"longitude": 32.7203, "latitude": 26.1551, "timezone": 2},
    "sohag": {"longitude": 31.6927, "latitude": 26.5590, "timezone": 2},
    "hurghada": {"longitude": 33.7984, "latitude": 27.2579, "timezone": 2},
    "sharm el sheikh": {"longitude": 34.3299, "latitude": 27.9158, "timezone": 2},
    "tanta": {"longitude": 31.0027, "latitude": 30.7865, "timezone": 2},
    "damanhur": {"longitude": 30.4720, "latitude": 31.0358, "timezone": 2},
    "el mahalla el kubra": {"longitude": 31.1711, "latitude": 30.9706, "timezone": 2},
    "beni mazar": {"longitude": 30.7551, "latitude": 28.4958, "timezone": 2},
    "kafr el sheikh": {"longitude": 30.9406, "latitude": 31.1117, "timezone": 2},
    "riyadh": {"longitude": 46.6753, "latitude": 24.7136, "timezone": 3},
    "jeddah": {"longitude": 39.1979, "latitude": 21.4858, "timezone": 3},
    "mecca": {"longitude": 39.8579, "latitude": 21.3891, "timezone": 3},
    "medina": {"longitude": 39.6111, "latitude": 24.5247, "timezone": 3},
    "dammam": {"longitude": 50.0986, "latitude": 26.3927, "timezone": 3},
    "tabuk": {"longitude": 36.5550, "latitude": 28.3838, "timezone": 3},
    "khobar": {"longitude": 50.1911, "latitude": 26.2172, "timezone": 3},
    "buraydah": {"longitude": 43.9750, "latitude": 26.3259, "timezone": 3},
    "hail": {"longitude": 41.6981, "latitude": 27.5114, "timezone": 3},
    "abha": {"longitude": 42.5053, "latitude": 18.2465, "timezone": 3},
    "najran": {"longitude": 44.1277, "latitude": 17.4915, "timezone": 3},
    "jizan": {"longitude": 42.5461, "latitude": 16.8890, "timezone": 3},
    "al_bahah": {"longitude": 41.4426, "latitude": 20.0129, "timezone": 3},
    "sakaka": {"longitude": 40.2064, "latitude": 29.9697, "timezone": 3},
    "arar": {"longitude": 41.0155, "latitude": 30.9753, "timezone": 3},
    "tripoli": {"longitude": 13.1873, "latitude": 32.8872, "timezone": 2},
    "benghazi": {"longitude": 20.0648, "latitude": 32.1189, "timezone": 2},
    "misrata": {"longitude": 15.0901, "latitude": 32.3754, "timezone": 2},
    "sabha": {"longitude": 14.4283, "latitude": 27.0377, "timezone": 2},
    "al_bayda": {"longitude": 21.7350, "latitude": 32.7627, "timezone": 2},
    "zawiya": {"longitude": 12.7278, "latitude": 32.7596, "timezone": 2},
    "ajdabiya": {"longitude": 20.2140, "latitude": 30.7522, "timezone": 2},
    "derna": {"longitude": 22.6393, "latitude": 32.7680, "timezone": 2},
    "geryan": {"longitude": 13.0203, "latitude": 32.1722, "timezone": 2},
    "zintan": {"longitude": 12.7958, "latitude": 31.9315, "timezone": 2},
    "new_york": {"longitude": -74.0060, "latitude": 40.7128, "timezone": -5},
    "los_angeles": {"longitude": -118.2437, "latitude": 34.0522, "timezone": -8},
    "london": {"longitude": -0.1276, "latitude": 51.5074, "timezone": 0},
    "paris": {"longitude": 2.3522, "latitude": 48.8566, "timezone": 1},
    "berlin": {"longitude": 13.4050, "latitude": 52.5200, "timezone": 1},
    "tokyo": {"longitude": 139.6917, "latitude": 35.6895, "timezone": 9},
    "beijing": {"longitude": 116.4074, "latitude": 39.9042, "timezone": 8},
    "moscow": {"longitude": 37.6173, "latitude": 55.7558, "timezone": 3},
    "sydney": {"longitude": 151.2093, "latitude": -33.8688, "timezone": 11},
    "cape_town": {"longitude": 18.4241, "latitude": -33.9249, "timezone": 2},
    "toronto": {"longitude": -79.3832, "latitude": 43.6511, "timezone": -5},
    "buenos_aires": {"longitude": -58.3816, "latitude": -34.6037, "timezone": -3},
    "mumbai": {"longitude": 72.8777, "latitude": 19.0760, "timezone": 5.5},
    "dubai": {"longitude": 55.2708, "latitude": 25.2760, "timezone": 4},
    "bangkok": {"longitude": 100.5018, "latitude": 13.7563, "timezone": 7},
    "singapore": {"longitude": 103.8198, "latitude": 1.3521, "timezone": 8},
    "nairobi": {"longitude": 36.8219, "latitude": -1.2864, "timezone": 3},
    "mexico_city": {"longitude": -99.1332, "latitude": 19.4326, "timezone": -6},
    "santiago": {"longitude": -70.6483, "latitude": -33.4489, "timezone": -4}
}

app(main)
