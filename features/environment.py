from behave import fixture, use_fixture
from splinter.browser import Browser

@fixture
def splinter_browser(context):
    context.browser = Browser(driver_name="remote",
                              url='http://firefox:4444/wd/hub',
                              browser='firefox')
    yield context.browser
    context.browser.quit()

def before_all(context):
    context.base_url = 'http://test:8000'
    use_fixture(splinter_browser, context)

# def before_scenario(context, scenario):
#     import pdb; pdb.set_trace()
