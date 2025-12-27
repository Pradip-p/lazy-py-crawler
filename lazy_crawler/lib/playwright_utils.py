from playwright_stealth import stealth_async


async def init_page(page, request):
    """
    Callback to initialize Playwright page with stealth and other advanced settings.
    """
    await stealth_async(page)
    # Add other page-level configurations here if needed
    # e.g., setting extra headers, masking automation, etc.
