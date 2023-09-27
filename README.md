# TradovateTradingBot
Automated trading bot that won't ever make you money

I wanted to automate a way to make trades for me while I wasn't staring at my computer for multiple hours a day, and since I was only trading based on basic candlestick patterns, this task wasn't going to be that hard. I used the broker, Tradovate, so if you ever want to try this out then you'd need the same broker. I didn't want to pay for the API so this automation is based around computer screenshots. 

Here is how it works and if you'd like to try it out. Feel free!

1. A region for screenshots will need to be specified because the program is set for my computer's resolution which is 1920x1080. pyautogui takes the screenshot for us, we just need to specify a region on the screen for it to capture, using pixel values. If this is what your tradovate layout looks like...

![TraderScreen](https://github.com/kjcingel/TradovateTradingBot/assets/123612146/762ed014-7e80-4e9e-858e-33f6d19abe70)

You want to position the screenshot so that it is in a spot to capture only candles and a black background. Like this

![IdealScreen](https://github.com/kjcingel/TradovateTradingBot/assets/123612146/e0a76a60-f626-4e8e-8f23-e7fbbb4cedb7)

The capture size of the screenshot is found in the screenshot() function. The values you may need to change are left, top, width, and height in that order. Left is the amount of pixels from the left side on the screen and top is the amount of pixels from the top of the screen. 

![ScreenshotFunction](https://github.com/kjcingel/TradovateTradingBot/assets/123612146/b464a6c1-07d2-47cd-a5d3-44f8087c0f81)

2. You will need to create a stop loss/take profit order setting so that when you buy market or sell market is pressed, 2 points are now added to your screen which are the stop loss and take profit. If either points are hit during an active trade, a new order will be placed and your trade will be exited. The stop loss point if hit, means you lost on that trade, and the take profit point if hit means you've won on the trade. Find the spot labeled ATM and click the cog.

![StopLossLocation](https://github.com/kjcingel/TradovateTradingBot/assets/123612146/165f402f-d5f7-42e3-85de-6f6c1376f1c4)

The cog will bring you to the settings and you must create a preset for a stop loss/ take profit ATM. Copy my settings and make sure the preset is selected next to the ATM label.

![StopLossSettings](https://github.com/kjcingel/TradovateTradingBot/assets/123612146/443b07e4-3211-4b69-9131-2bb8137bd247)

3. After that you should be good to go. The program takes trades when there is an engulfing candle either bullish or bearish. You can test individual functions by commenting out the while loop and running each one through. I recommend doing this so you know that everything is working properly. Unfortunately This will never make you money because candlestick patterns alone won't be enough to give you any indication of a winning trade but it is fun to watch trades be made for you.
