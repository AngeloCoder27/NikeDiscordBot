from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from discord.ext import commands, tasks
from discord import Embed, Colour, Intents
from json import load, dump
import time

# Initialize the bot with the desired prefix and intents
bot = commands.Bot(command_prefix='!', intents=Intents.all())

# Path to store data
data_path = "nike_data.json"

# Load initial settings and data from JSON
with open(data_path, "r") as f:
    data = load(f)
    show_discount_shoes = data.get("show_discount_shoes", True)
    last_seen = data.get("last_seen", [])
    channels = data.get("channels", [])

seen = []
discount = {}  # Shoes with a discount

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode

# Path to ChromeDriver
service = Service('/home/angelocoder27/chromedriver-linux64/chromedriver')

# Set up the WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)


def get_nike_discounts():
    url = "https://www.nike.com/ph/w/sale-3yaep"
    driver.get(url)

    # Allow some time for the page to load
    time.sleep(5)

    sales = {}

    product_cards = driver.find_elements(By.CSS_SELECTOR, 'div.product-card')

    for card in product_cards:
        try:
            name_tag = card.find_element(By.CSS_SELECTOR, 'div.product-card__title')
            price_tag = card.find_element(By.CSS_SELECTOR, 'div.product-card__price')
            image_tag = card.find_element(By.CSS_SELECTOR, 'img.product-card__hero-image')
            link_tag = card.find_element(By.CSS_SELECTOR, 'a.product-card__link-overlay')

            name = name_tag.text.strip()
            price = price_tag.text.strip()
            image_url = image_tag.get_attribute('src')
            product_link = link_tag.get_attribute('href')

            if image_url.startswith("data:image"):
                print(f"Data URL detected for {name}")
                image_url = None
            elif not image_url.startswith("http"):
                image_url = None

            # Separate original and discounted prices
            if "₱" in price:
                prices = price.split("₱")
                if len(prices) == 3:
                    original_price = f"~~₱{prices[2].strip()}~~"
                    discounted_price = f"₱{prices[1].strip()}"
                    formatted_price = f"{original_price} {discounted_price}"
                else:
                    formatted_price = price
            else:
                formatted_price = price

            # Store the details in the dictionary
            sales[name] = (formatted_price, image_url, product_link)
        except Exception as e:
            print(f"Error processing a product card: {e}")

    return sales

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user.name} (ID: {bot.user.id})')
    await check_for_discount.start()


@bot.command(name='discount')
async def show_discounts(ctx):
    """Shows current Nike discounts in the channel."""
    discounts = get_nike_discounts()

    if discounts:
        for name, (price, image_url, product_link) in discounts.items():
            embed = Embed(
                title=name,
                colour=Colour.from_rgb(232, 17, 35),
                description=f"Price: {price}\n[Click Here to Purchase!]({product_link})"
            )

            if image_url:
                embed.set_image(url=image_url)  # Add the image URL if it's valid

            await ctx.send(embed=embed)
    else:
        await ctx.send("No discounts available at the moment.")

@bot.command()
async def add_channel(ctx, channel_id: int = None):
    """Adds a channel to the notification list."""
    if channel_id is None:
        channel_id = ctx.channel.id

    if channel_id not in channels:
        channels.append(channel_id)
        with open(data_path, "r+") as file:
            data = load(file)
            data['channels'].append(channel_id)
            file.seek(0)
            dump(data, file, indent=2)
            file.truncate()
        await ctx.send(f"Channel (ID: {channel_id}) added to the notification list")
    else:
        await ctx.send("Channel is already in the notification list.")


@bot.command()
async def remove_channel(ctx, channel_id: int = None):
    """Removes a channel from the notification list."""
    if channel_id is None:
        channel_id = ctx.channel.id

    if channel_id in channels:
        channels.remove(channel_id)
        with open(data_path, "r+") as file:
            data = load(file)
            data['channels'].remove(channel_id)
            file.seek(0)
            dump(data, file, indent=2)
            file.truncate()
        await ctx.send(f"Channel (ID: {channel_id}) removed from the notification list")
    else:
        await ctx.send("Channel is not in the notification list.")


@tasks.loop(minutes=60)
async def check_for_discount():
    global last_seen, seen

    discounts = get_nike_discounts()

    for name, (price, image_url, product_link) in discounts.items():
        if name not in last_seen:
            last_seen.append(name)
            seen.append(name)
            discount[name] = (price, image_url, product_link)

            embed = Embed(
                colour=Colour.from_rgb(232, 17, 35),
                title=name,
                url="https://www.nike.com/ph/w/sale-3yaep",
                description=f"Price: {price}\n[Click Here to Purchase]({product_link})"
            )

            if image_url:
                embed.set_image(url=image_url)

            for channel_id in channels:
                channel = bot.get_channel(channel_id)
                if channel:
                    await channel.send(embed=embed)

    last_seen = seen
    seen = []

    # Save updated data back to the JSON file
    with open(data_path, "w") as file:
        dump({
            "last_seen": last_seen,
            "show_discount_shoes": show_discount_shoes,
            "channels": channels
        }, file, indent=2)


# Make sure to quit the driver when your bot is shutting down
@bot.event
async def on_disconnect():
    driver.quit()

# Run the bot with your bot token
bot.run('')
