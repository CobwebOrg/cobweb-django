from django.urls import reverse


@given("I'm not logged in")
def step_impl(context):
    context.browser.visit('http://test:8000/' + reverse("logout"))


@when('I visit {url}')
def step_impl(context, url):
    if url == 'any page':
        url = reverse('front_page')
    context.browser.visit('http://test:8000' + url)


@then('the text "{text}" links to {url_name}')
def step_impl(context, text, url_name):
    links = context.browser.find_by_xpath(f'//a[text()="{text}"]/')
    assert len(links) == 1
    assert links[0].text == 'Sign Up'
    target = 'http://test:8000' + reverse('user_create')
    context.test.assertEqual(links[0]['href'][:len(target)], target)


@when('I click the "sign up" link')
def step_impl(context):
    context.browser.find_by_text('Sign Up')[0].click()


@then('taken to {url_name} page')
def step_impl(context, url_name):
    context.test.assertTrue(
        context.browser.url.startswith('http://test:8000'+reverse(url_name))
    )


@then(u'the text "{text}" does not appear as a link')
def step_impl(context, text):
    context.test.assertTrue(
        context.browser.is_element_not_present_by_xpath("//a[text()='{text}'")
    )


@then(u'I get redirected to a the login page')
def step_impl(context):
    target = 'http://test:8000' + reverse('login')
    context.test.assertTrue(
        context.browser.url
    )


@then(u'I get an error message telling me I need to log in')
def step_impl(context):
    context.test.assertIn(context.browser.html, 'Please login to see this page.')


@given(u'I am logged in')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I\'m a logged in user')
