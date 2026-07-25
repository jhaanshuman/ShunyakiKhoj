from datetime import datetime, timedelta
from typing import List, Any
from .dasha_base import DashaPeriod

YOGINIS = ['Mangala', 'Pingala', 'Dhanya', 'Bhramari', 'Bhadrika', 'Ulka', 'Siddha', 'Sankata']
YEARS = [1, 2, 3, 4, 5, 6, 7, 8] # Total 36 years cycle

def calculate_yogini(master_obj: Any) -> List[dict]:
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
    
    start_yogini_idx = (nak_idx + 3) % 8
    lord_duration = YEARS[start_yogini_idx]
    elapsed_years = offset * lord_duration
    
    start_dt = birth_dt - timedelta(days=elapsed_years * 365.2425)
    now_dt = datetime.now()
    
    periods = []
    current_dt = start_dt
    
    for i in range(8):
        idx = (start_yogini_idx + i) % 8
        yogini_name = YOGINIS[idx]
        yr = YEARS[idx]
        
        m_start = current_dt
        m_end = current_dt + timedelta(days=yr * 365.2425)
        current_dt = m_end
        
        age_start = (m_start - birth_dt).days / 365.2425
        age_end = (m_end - birth_dt).days / 365.2425
        
        is_current = (m_start <= now_dt <= m_end)
        is_upcoming = (m_start > now_dt)
        
        period = DashaPeriod(
            start_year=round(m_start.year + (m_start.timetuple().tm_yday / 365.25), 2),
            end_year=round(m_end.year + (m_end.timetuple().tm_yday / 365.25), 2),
            start_date=m_start,
            end_date=m_end,
            age_start=round(age_start, 2),
            age_end=round(age_end, 2),
            duration_years=yr,
            lord=yogini_name,
            is_current=is_current,
            is_upcoming=is_upcoming
        )
        periods.append(period.to_dict())
        
    return periods
