# Online Marketplace (gRPC)

This project implements a simple online marketplace using gRPC for communication between the market server and seller/buyer clients.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)

## Features
- Seller registration
- Item listing by sellers
- Item search by buyers
- Buying items
- Adding items to wish list
- Rating items
- Notifications to sellers and buyers
- Displaying seller items

## Prerequisites
- Python 3.x
- gRPC (install using `pip install grpcio`)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/online-marketplace.git
   ```
2. Navigate to the project directory
   ```bash
   cd Online-Marketplace--gRPC-/
   ```
3. Install the required dependencies:
   ```bash
   pip install grpcio
   ```

## Usage
1. Run the central platform:
   ```bash
   python3 market.py
   ```
2. Open separate terminals for each seller and buyer.
   For each seller, run:
   ```bash
   python3 seller.py
   ```
   ```bash
   python3 client.py
   ```
3. Follow the seller and buyer terminal prompts to interact with the marketplace.

## Project Structure

- **central_platform.py**: Handles seller registration, item listing, and notifications.

- **seller.py**: Seller client for adding items, receiving notifications, and displaying seller items.

- **client.py**: Buyer client for searching, buying, wish list management, rating, and notifications.

- **readme.md**: Project documentation with installation, usage, and project structure details.

## Overview

This online marketplace demonstrates gRPC functionality with features including:
- Seller registration
- Item listing
- Buying items
- Managing wish lists
- Rating items
- Notifications for both sellers and buyers

The project is structured to maintain a clear separation of concerns between the central platform, sellers, and buyers.
