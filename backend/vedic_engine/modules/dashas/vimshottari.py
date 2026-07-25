from datetime import datetime, timedelta
from typing import List, Any
from .dasha_base import DashaPeriod

LORDS = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
YEARS = [7, 20, 6, 10, 7, 18, 16, 19, 17]

def calculate_vimshottari(master_obj: Any) -> List[dict]:
    planets = master_obj.get('planets', {})
    moon_data = planets.get('Moon', {})
    moon_lon = moon_data.get('sidereal_lon', 120.0)
    
    meta = master_obj.get('metadata', {})
    birth_details = meta.get('birth_details', {}) if isinstance(meta, dict) else {}
    dob_str = birth_details.get('date', '1994/01/05')
    tob_str = birth_details.get('time', '12:00')
    
    try:
        parts = str(dob_str).replace('-', '/').split('/')
        t_parts = str(tob_str).split(':')
        birth_dt = datetime(int(parts[0]), int(parts[1]), int(parts[2]), int(t_parts[0]), int(t_parts[1]))
    except Exception:
        birth_dt = datetime(1994, 1, 5, 12, 0)
        
    nak_size = 13.333333333333334
    nak_idx = int(moon_lon / nak_size) % 27
    offset = (moon_lon - (nak_idx * nak_size)) / nak_size
    
    start_lord_idx = nak_idx % 9
    lord_duration = YEARS[start_lord_idx]
    elapsed_years = offset * lord_duration
    
    start_dt = birth_dt - timedelta(days=elapsed_years * 365.2425)
    now_dt = datetime.now()
    
    mahadashas = []
    current_dt = start_dt
    
    for i in range(9):
        idx = (start_lord_idx + i) % 9
        lord = LORDS[idx]
        yr = YEARS[idx]
        
        m_start = current_dt
        m_end = current_dt + timedelta(days=yr * 365.2425)
        current_dt = m_end
        
        age_start = (m_start - birth_dt).days / 365.2425
        age_end = (m_end - birth_dt).days / 365.2425
        
        is_current = (m_start <= now_dt <= m_end)
        is_upcoming = (m_start > now_dt)
        
        antardashas = []
        sub_current_dt = m_start
        for j in range(9):
            sub_idx = (idx + j) % 9
            sub_lord = LORDS[sub_idx]
            sub_yr = YEARS[sub_idx]
            sub_duration_days = (yr * sub_yr / 120.0) * 365.2425
            
            sub_start = sub_current_dt
            sub_end = sub_start + timedelta(days=sub_duration_days)
            sub_current_dt = sub_end
            
            sub_is_current = (sub_start <= now_dt <= sub_end)
            sub_is_upcoming = (sub_start > now_dt)
            
            antardashas.append({
                "lord": f"{lord}-{sub_lord}",
                "mahadasha_lord": lord,
                "antardasha_lord": sub_lord,
                "duration_years": round((yr * sub_yr / 120.0), 3),
                "start_date": sub_start.strftime("%Y-%m-%d"),
                "end_date": sub_end.strftime("%Y-%m-%d"),
                "is_current": sub_is_current,
                "is_upcoming": sub_is_upcoming
            })
            
        period = DashaPeriod(
            start_year=round(m_start.year + (m_start.timetuple().tm_yday / 365.25), 2),
            end_year=round(m_end.year + (m_end.timetuple().tm_yday / 365.25), 2),
            start_date=m_start,
            end_date=m_end,
            age_start=round(age_start, 2),
            age_end=round(age_end, 2),
            duration_years=yr,
            lord=lord,
            is_current=is_current,
            is_upcoming=is_upcoming,
            sub_periods=[
                DashaPeriod(
                    start_year=round(datetime.strptime(a["start_date"], "%Y-%m-%d").year, 2),
                    end_year=round(datetime.strptime(a["end_date"], "%Y-%m-%d").year, 2),
                    start_date=datetime.strptime(a["start_date"], "%Y-%m-%d"),
                    end_date=datetime.strptime(a["end_date"], "%Y-%m-%d"),
                    age_start=0.0,
                    age_end=0.0,
                    duration_years=a["duration_years"],
                    lord=a["lord"],
                    is_current=a["is_current"],
                    is_upcoming=a["is_upcoming"]
                ) for a in antardashas
            ]
        )
        mahadashas.append(period.to_dict())
        
    return mahadashas
