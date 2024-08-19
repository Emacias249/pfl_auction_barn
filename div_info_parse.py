import re
from bs4 import BeautifulSoup

def find_horse_stats(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    if len(lines) < 4:
        raise Exception("The file does not contain enough lines")
    
    # Extract the first line for the scraping URL
    first_line = lines[0].strip()
    scraping_url = None
    if first_line.startswith("Scraping URL:"):
        scraping_url = first_line[len("Scraping URL:"):].strip()
        print(f"Horse URL: {scraping_url}")
    
    # Extract the second line
    second_line = lines[3].strip()
    
    # Initialize variables with default values
    horse_name = "Not Found"
    career_summary_stats = "Not Found"
    career_earnings = "Not Found"
    image_url = "Not Found"
    racing_direction = "Not Found"
    racing_surface = "Not Found"
    racing_condition = "Not Found"
    stable_name = "Not Found"
    
    for part in second_line.split('\n'):
        if part.startswith("HTML:"):
            html_content = part[len("HTML:"):].strip()
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Use BeautifulSoup to find the horse name in the specified span format
            horse_name_span = soup.find('span', class_='text-2xl')
            if horse_name_span:
                horse_name = horse_name_span.get_text(strip=True)
            
            # Extract career stats from the specified <p> tag
            career_summary_p = soup.find('p', class_='text-sm text-white font-inter')
            if career_summary_p:
                career_summary_stats = career_summary_p.get_text(strip=True)
            
            # Extract career earnings from the specified <p> tag
            career_earnings_p = soup.find('p', class_='text-sm text-slate-300')
            if career_earnings_p:
                career_earnings = career_earnings_p.get_text(strip=True)
            
            # Extract the image URL from the <img> tag
            img_tag = soup.find('img', alt='Horse Portrait')
            if img_tag and img_tag.has_attr('src'):
                image_url = img_tag['src']
            
            # Extract Racing Direction, Racing Surface, and Racing Condition
            p_tags = soup.find_all('p', class_='text-sm text-white/75')
            if len(p_tags) >= 3:
                racing_direction = p_tags[0].get_text(strip=True)
                racing_surface = p_tags[1].get_text(strip=True)
                racing_condition = p_tags[2].get_text(strip=True)
            
            # Extract the stable name from the specified <a> tag
            stable_name_a = soup.find('a', class_='text-secondary-100/80 hover:text-secondary-400 underline block pl-1 cursor-pointer')
            if stable_name_a:
                stable_name = stable_name_a.get_text(strip=True)
                
    return (horse_name, scraping_url, career_summary_stats, career_earnings, 
            image_url, racing_direction, racing_surface, racing_condition, 
            stable_name)

# Example usage
file_path = 'div_info.txt'
results = find_horse_stats(file_path)
horse_name, scraping_url, career_summary_stats, career_earnings, image_url, racing_direction, racing_surface, racing_condition, stable_name = results

print(f"Horse Name: {horse_name}")
print(f"Stable Name: {stable_name}")
print(f"Horse URL: {scraping_url if scraping_url else 'Not Found'}")
print(f"Career Summary: {career_summary_stats}")
print(f"Career Earnings: {career_earnings}")
print(f"Image URL: {image_url}")
print(f"Racing Direction: {racing_direction}")
print(f"Racing Surface: {racing_surface}")
print(f"Racing Condition: {racing_condition}")

