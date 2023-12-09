# IGNORE THIS!!!
# This file is NOT a part of the system.
# It exists only to make things easier for myself when working on this, or returning to this in the future. 

# CMDs: =====================================================================================================================

    # python manage.py makemigrations
    # python manage.py migrate

    # python.exe -m venv .venv
    # .\.venv\Scripts\activate
    # pip freeze > requirements.txt
    # pip install -r requirements.txt 

    # Use the line below after running 'npm run build'
        # python manage.py collectstatic

    # Superuser:
        # username: Cat
        # password: Murka1234

    # pytest ./tests/airline_reservation_system/test_utiles.py::Test_Populate_All
    # pytest ./tests/airline_reservation_system/test_utiles.py::Test_Val_Add_User
    # pytest ./tests/airline_reservation_system/test_utiles.py::Test_For_Missing_Migrations

    # React:
        # before deployment: npm run build 
        # for deployment use: npm start build 

    # Set the API counter manually:
        # python manage.py set_apicounter <value>

# ===========================================================================================================================
# 95% --> Django refs:

    # in TF: https://docs.djangoproject.com/en/4.2/topics/
    # in VF: https://www.youtube.com/playlist?list=PLaUQIPIyD0z73qS-7zKIbRnpucKOCVnBi
    # https://stackoverflow.com/questions/448271/what-is-init-py-for
    # https://www.geeksforgeeks.org/how-to-create-superuser-in-django/
    # https://stackoverflow.com/questions/55940630/how-to-execute-code-automatically-after-manage-py-runserver
    # https://stackoverflow.com/questions/6791911/execute-code-when-django-starts-once-only
    # https://stackoverflow.com/questions/73587720/django-test-to-check-for-pending-migrations


# ===========================================================================================================================
# models, DB and query refs:

    # https://www.geeksforgeeks.org/creating-custom-user-model-using-abstractuser-in-django_restframework/
    # https://docs.djangoproject.com/en/4.2/ref/models/options/
    # https://docs.djangoproject.com/en/4.2/ref/models/constraints/
    # https://stackoverflow.com/questions/3647805/get-models-fields-in-django
    # https://docs.djangoproject.com/en/4.2/topics/db/queries/
    # https://www.youtube.com/watch?v=H0XCXCtSKYE&list=PLaUQIPIyD0z73qS-7zKIbRnpucKOCVnBi&index=18 (m.m joins)
    # https://stackoverflow.com/questions/25890406/django-join-two-models
    # https://www.youtube.com/watch?v=-64bh0uitG4&list=PLaUQIPIyD0z73qS-7zKIbRnpucKOCVnBi&index=19 (Q)

    # filter queries '__x':
        #  __lte --> Less than or equal     <=
        #  __gte --> Greater than or equal  >=
        #  __lt --> Less than               <
        #  __gt --> Greater than            >

    # https://stackoverflow.com/questions/26672077/django-model-vs-model-objects-create
    # https://stackoverflow.com/questions/34704512/accessing-models-by-variable-model-name-in-django
    # https://stackoverflow.com/questions/1164930/image-resizing-with-django/1164988#1164988
    # https://stackoverflow.com/questions/8373571/using-height-field-and-width-field-attribute-in-imagefield-of-django
    # https://stackoverflow.com/questions/40520797/how-to-find-height-and-width-of-image-for-filefield-django?rq=3
    # https://stackoverflow.com/questions/57111648/how-to-resize-an-imagefield-image-before-saving-it-in-python-django-model
    # https://pypi.org/project/django-resized/
    # https://stackoverflow.com/questions/70839890/pil-remove-error-userwarning-palette-images-with-transparency-expressed-in-byt
    # https://stackoverflow.com/questions/1276887/default-image-for-imagefield-in-djangos-orm   
    # https://stackoverflow.com/questions/74641318/how-to-save-a-resized-image-in-django    
    # https://stackoverflow.com/questions/20469174/whats-the-difference-between-staff-admin-superuser-in-django
    # https://stackoverflow.com/questions/1885101/delete-data-from-all-tables-in-mysql
    # https://stackoverflow.com/questions/2995054/access-denied-for-user-rootlocalhost-using-passwordno
    # https://stackoverflow.com/questions/28613102/last-login-field-is-not-updated-when-authenticating-using-tokenauthentication-in
    # https://stackoverflow.com/questions/47182481/dynamic-filter-in-django
    # https://stackoverflow.com/questions/45190151/there-is-a-way-to-check-if-a-model-field-contains-a-substring

    # RANDOM DATA GENERATORS:
        # https://jimpix.co.uk/words/random-username-list.asp
        # https://www.randomlists.com/email-addresses
        # https://delinea.com/resources/password-generator-it-tool  
        # https://randommer.io/Phone
        # https://www.vccgenerator.org/
        # https://www.randomlists.com/random-names
        # https://www.randomlists.com/random-addresses


# ===========================================================================================================================
# flag ref: (Not obligatory. Will implement this only if I'll have time.)

    # https://flagpedia.net/download/api
    # https://stackoverflow.com/questions/30229231/python-save-image-from-url
    # https://stackoverflow.com/questions/19573809/open-images-from-a-folder-one-by-one-using-python
    # https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
    # https://gist.github.com/rogerallen/1583606 :
    # country_to_abbrev = {
    #     "Andorra": "AD",
    #     "United Arab Emirates": "AE",
    #     "Afghanistan": "AF",
    #     "Antigua and Barbuda": "AG",
    #     "Anguilla": "AI",
    #     "Albania": "AL",
    #     "Armenia": "AM",
    #     "Angola": "AO",
    #     "Antarctica": "AQ",
    #     "Argentina": "AR",
    #     "American Samoa": "AS",
    #     "Austria": "AT",
    #     "Australia": "AU",
    #     "Aruba": "AW",
    #     "Åland Islands": "AX",
    #     "Azerbaijan": "AZ",
    #     "Bosnia and Herzegovina": "BA",
    #     "Barbados": "BB",
    #     "Bangladesh": "BD",
    #     "Belgium": "BE",
    #     "Burkina Faso": "BF",
    #     "Bulgaria": "BG",
    #     "Bahrain": "BH",
    #     "Burundi": "BI",
    #     "Benin": "BJ",
    #     "Saint Barthélemy": "BL",
    #     "Bermuda": "BM",
    #     "Brunei Darussalam": "BN",
    #     "Bolivia (Plurinational State of)": "BO",
    #     "Bonaire, Sint Eustatius and Saba": "BQ",
    #     "Brazil": "BR",
    #     "Bahamas": "BS",
    #     "Bhutan": "BT",
    #     "Bouvet Island": "BV",
    #     "Botswana": "BW",
    #     "Belarus": "BY",
    #     "Belize": "BZ",
    #     "Canada": "CA",
    #     "Cocos (Keeling) Islands": "CC",
    #     "Congo, Democratic Republic of the": "CD",
    #     "Central African Republic": "CF",
    #     "Congo": "CG",
    #     "Switzerland": "CH",
    #     "Côte d'Ivoire": "CI",
    #     "Cook Islands": "CK",
    #     "Chile": "CL",
    #     "Cameroon": "CM",
    #     "China": "CN",
    #     "Colombia": "CO",
    #     "Costa Rica": "CR",
    #     "Cuba": "CU",
    #     "Cabo Verde": "CV",
    #     "Curaçao": "CW",
    #     "Christmas Island": "CX",
    #     "Cyprus": "CY",
    #     "Czechia": "CZ",
    #     "Germany": "DE",
    #     "Djibouti": "DJ",
    #     "Denmark": "DK",
    #     "Dominica": "DM",
    #     "Dominican Republic": "DO",
    #     "Algeria": "DZ",
    #     "Ecuador": "EC",
    #     "Estonia": "EE",
    #     "Egypt": "EG",
    #     "Western Sahara": "EH",
    #     "Eritrea": "ER",
    #     "Spain": "ES",
    #     "Ethiopia": "ET",
    #     "Finland": "FI",
    #     "Fiji": "FJ",
    #     "Falkland Islands (Malvinas)": "FK",
    #     "Micronesia (Federated States of)": "FM",
    #     "Faroe Islands": "FO",
    #     "France": "FR",
    #     "Gabon": "GA",
    #     "United Kingdom of Great Britain and Northern Ireland": "GB",
    #     "Grenada": "GD",
    #     "Georgia": "GE",
    #     "French Guiana": "GF",
    #     "Guernsey": "GG",
    #     "Ghana": "GH",
    #     "Gibraltar": "GI",
    #     "Greenland": "GL",
    #     "Gambia": "GM",
    #     "Guinea": "GN",
    #     "Guadeloupe": "GP",
    #     "Equatorial Guinea": "GQ",
    #     "Greece": "GR",
    #     "South Georgia and the South Sandwich Islands": "GS",
    #     "Guatemala": "GT",
    #     "Guam": "GU",
    #     "Guinea-Bissau": "GW",
    #     "Guyana": "GY",
    #     "Hong Kong": "HK",
    #     "Heard Island and McDonald Islands": "HM",
    #     "Honduras": "HN",
    #     "Croatia": "HR",
    #     "Haiti": "HT",
    #     "Hungary": "HU",
    #     "Indonesia": "ID",
    #     "Ireland": "IE",
    #     "Israel": "IL",
    #     "Isle of Man": "IM",
    #     "India": "IN",
    #     "British Indian Ocean Territory": "IO",
    #     "Iraq": "IQ",
    #     "Iran (Islamic Republic of)": "IR",
    #     "Iceland": "IS",
    #     "Italy": "IT",
    #     "Jersey": "JE",
    #     "Jamaica": "JM",
    #     "Jordan": "JO",
    #     "Japan": "JP",
    #     "Kenya": "KE",
    #     "Kyrgyzstan": "KG",
    #     "Cambodia": "KH",
    #     "Kiribati": "KI",
    #     "Comoros": "KM",
    #     "Saint Kitts and Nevis": "KN",
    #     "Korea (Democratic People's Republic of)": "KP",
    #     "Korea, Republic of": "KR",
    #     "Kuwait": "KW",
    #     "Cayman Islands": "KY",
    #     "Kazakhstan": "KZ",
    #     "Lao People's Democratic Republic": "LA",
    #     "Lebanon": "LB",
    #     "Saint Lucia": "LC",
    #     "Liechtenstein": "LI",
    #     "Sri Lanka": "LK",
    #     "Liberia": "LR",
    #     "Lesotho": "LS",
    #     "Lithuania": "LT",
    #     "Luxembourg": "LU",
    #     "Latvia": "LV",
    #     "Libya": "LY",
    #     "Morocco": "MA",
    #     "Monaco": "MC",
    #     "Moldova, Republic of": "MD",
    #     "Montenegro": "ME",
    #     "Saint Martin (French part)": "MF",
    #     "Madagascar": "MG",
    #     "Marshall Islands": "MH",
    #     "North Macedonia": "MK",
    #     "Mali": "ML",
    #     "Myanmar": "MM",
    #     "Mongolia": "MN",
    #     "Macao": "MO",
    #     "Northern Mariana Islands": "MP",
    #     "Martinique": "MQ",
    #     "Mauritania": "MR",
    #     "Montserrat": "MS",
    #     "Malta": "MT",
    #     "Mauritius": "MU",
    #     "Maldives": "MV",
    #     "Malawi": "MW",
    #     "Mexico": "MX",
    #     "Malaysia": "MY",
    #     "Mozambique": "MZ",
    #     "Namibia": "NA",
    #     "New Caledonia": "NC",
    #     "Niger": "NE",
    #     "Norfolk Island": "NF",
    #     "Nigeria": "NG",
    #     "Nicaragua": "NI",
    #     "Netherlands": "NL",
    #     "Norway": "NO",
    #     "Nepal": "NP",
    #     "Nauru": "NR",
    #     "Niue": "NU",
    #     "New Zealand": "NZ",
    #     "Oman": "OM",
    #     "Panama": "PA",
    #     "Peru": "PE",
    #     "French Polynesia": "PF",
    #     "Papua New Guinea": "PG",
    #     "Philippines": "PH",
    #     "Pakistan": "PK",
    #     "Poland": "PL",
    #     "Saint Pierre and Miquelon": "PM",
    #     "Pitcairn": "PN",
    #     "Puerto Rico": "PR",
    #     "Palestine, State of": "PS",
    #     "Portugal": "PT",
    #     "Palau": "PW",
    #     "Paraguay": "PY",
    #     "Qatar": "QA",
    #     "Réunion": "RE",
    #     "Romania": "RO",
    #     "Serbia": "RS",
    #     "Russian Federation": "RU",
    #     "Rwanda": "RW",
    #     "Saudi Arabia": "SA",
    #     "Solomon Islands": "SB",
    #     "Seychelles": "SC",
    #     "Sudan": "SD",
    #     "Sweden": "SE",
    #     "Singapore": "SG",
    #     "Saint Helena, Ascension and Tristan da Cunha": "SH",
    #     "Slovenia": "SI",
    #     "Svalbard and Jan Mayen": "SJ",
    #     "Slovakia": "SK",
    #     "Sierra Leone": "SL",
    #     "San Marino": "SM",
    #     "Senegal": "SN",
    #     "Somalia": "SO",
    #     "Suriname": "SR",
    #     "South Sudan": "SS",
    #     "Sao Tome and Principe": "ST",
    #     "El Salvador": "SV",
    #     "Sint Maarten (Dutch part)": "SX",
    #     "Syrian Arab Republic": "SY",
    #     "Eswatini": "SZ",
    #     "Turks and Caicos Islands": "TC",
    #     "Chad": "TD",
    #     "French Southern Territories": "TF",
    #     "Togo": "TG",
    #     "Thailand": "TH",
    #     "Tajikistan": "TJ",
    #     "Tokelau": "TK",
    #     "Timor-Leste": "TL",
    #     "Turkmenistan": "TM",
    #     "Tunisia": "TN",
    #     "Tonga": "TO",
    #     "Turkey": "TR",
    #     "Trinidad and Tobago": "TT",
    #     "Tuvalu": "TV",
    #     "Taiwan, Province of China": "TW",
    #     "Tanzania, United Republic of": "TZ",
    #     "Ukraine": "UA",
    #     "Uganda": "UG",
    #     "United States Minor Outlying Islands": "UM",
    #     "United States of America": "US",
    #     "Uruguay": "UY",
    #     "Uzbekistan": "UZ",
    #     "Holy See": "VA",
    #     "Saint Vincent and the Grenadines": "VC",
    #     "Venezuela (Bolivarian Republic of)": "VE",
    #     "Virgin Islands (British)": "VG",
    #     "Virgin Islands (U.S.)": "VI",
    #     "Viet Nam": "VN",
    #     "Vanuatu": "VU",
    #     "Wallis and Futuna": "WF",
    #     "Samoa": "WS",
    #     "Yemen": "YE",
    #     "Mayotte": "YT",
    #     "South Africa": "ZA",
    #     "Zambia": "ZM",
    #     "Zimbabwe": "ZW",
    # }
        
    # # invert the dictionary
    # abbrev_to_country = dict(map(reversed, country_to_abbrev.items()))


# ===========================================================================================================================
# log refs:

    # LEVELS [s=severity, 1=least | v=includes itself + all levels below it]:
        # DEBUG    --> s=1, v 
        # INFO     --> s=2, v
        # WARN     --> s=3, v
        # ERROR    --> s=4, v
        # CRITICAL --> s=5, v

    # https://www.youtube.com/watch?v=m_EkU56KdJg
    # https://docs.djangoproject.com/en/4.0/ref/logging/#default-logging-configuration
    # https://docs.python.org/3/library/logging.html#formatter-objects

    # https://stackoverflow.com/questions/40088496/how-to-use-pythons-rotatingfilehandler 
    # (^ "A RotatingFileHandler allows us to rotate our log statements into a new file every time the current log file reaches a certain size.")

    # (Propagate: Decides whether a log should be propagated to the logger's parent. By default, its value is True. If this attribute evaluates to true, 
    # events logged to this logger will be passed to the handlers of higher level (ancestor) loggers, in addition to any handlers attached to this logger.)

    # (filemode: This is an optional parameter specifying the mode in which you'd like to work with the log file specified by the parameter filename. 
    # Setting the file mode to it write ( w ) will overwrite the logs every time the module is run. Mode ( a ) will make it append new logs.)

# ===========================================================================================================================
# error-handling refs:

    # https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python
    # https://micropyramid.com/blog/custom-validations-for-serializer-fields-django-rest-framework

# ===========================================================================================================================
# validation refs:

    # https://bobbyhadz.com/blog/python-add-hours-to-datetime
    # credit card format only validation: https://stackoverflow.com/questions/9315647/regex-credit-card-number-tests (Won't use real credit card validation because then testing would become problematic and this isn't a project which would be used by real airlines anyways. And it wasn't even required.)
    # https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime
    # https://stackoverflow.com/questions/19970532/how-to-check-a-string-for-a-special-character
    # https://regexr.com/
    # https://stackoverflow.com/questions/3217682/how-to-validate-an-email-address-in-django
    # https://stackoverflow.com/questions/11456670/regular-expression-for-address-field-validation
    # https://ihateregex.io/expr/phone/#
    # https://stackoverflow.com/questions/11475885/python-replace-regex
    # https://ihateregex.io/expr/credit-card/
    # https://stackoverflow.com/questions/50504500/deprecationwarning-invalid-escape-sequence-what-to-use-instead-of-d
    # https://stackoverflow.com/questions/4415259/convert-regular-python-string-to-raw-string
    # https://stackoverflow.com/questions/2113908/what-regular-expression-will-match-valid-international-phone-numbers
    # https://stackoverflow.com/questions/20303252/django-rest-framework-imagefield?rq=3
    # https://stackoverflow.com/questions/889333/how-to-check-if-a-file-is-a-valid-image-file
    # https://stackoverflow.com/questions/16870663/how-do-i-validate-a-date-string-format-in-python?noredirect=1&lq=1
    # https://stackoverflow.com/questions/9987818/in-python-how-to-check-if-a-date-is-valid
    # https://stackoverflow.com/questions/16991948/detect-if-a-variable-is-a-datetime-object
    # https://stackoverflow.com/questions/10624937/convert-datetime-object-to-a-string-of-date-only-in-python
    # https://stackoverflow.com/questions/20010108/checking-if-username-exists-in-django
    # https://stackoverflow.com/questions/14894899/what-is-the-minimum-length-of-a-valid-international-phone-number
    # https://stackoverflow.com/questions/58006706/how-to-validate-phone-number-in-django
    # https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-a-phone-number-in-django-models
    # https://django-phonenumber-field.readthedocs.io/en/latest/reference.html#model-field
    # https://stackoverflow.com/questions/889333/how-to-check-if-a-file-is-a-valid-image-file
    # https://stackoverflow.com/questions/15307623/cant-compare-naive-and-aware-datetime-now-challenge-datetime-end

    # * max flight duration limit is set to 20 hours because: "Currently, the bragging rights for the longest flight in the world belong to Singapore Airlines' New York City to Singapore route. Its longest flight path, which connects Singapore's Changi Airport with New York's John F. Kennedy International Airport, 9,585 miles away, takes 18 hours and 40 minutes." (=~20h)
    # * min flight duration limit is set to 30 minutes because: "Taking the top prize for the world's shortest international airline route is the sector between Brazzaville (Congo Republic) and Kinshasa (The Democratic Republic of the Congo). The Congo River separates the two cities, and the distance between the two airports is just 13 miles. " + https://www.travelmath.com/flying-time/from/Brazzaville,+Congo/to/Kinshasa,+DR+Congo + "Not everyone is aware that the Congo is split into two entirely different countries—The Democratic Republic of the Congo (DRC), and the Republic of Congo." (and yes, this is one of the ways in which I procrastinate from actually coding.)
    # * max ticket number limit is set to 860 because: "Making the top spot in our list, the Airbus A380-800, a French-made passenger plane, has the capacity for 853 passengers in a single class or 644 in a two-tiered class and can travel up to 8,208 nautical miles or 15,200 kilometers." (=~860t)
    
    # https://stackoverflow.com/questions/510972/getting-the-class-name-of-an-instance


# ===========================================================================================================================
# view refs:

    # https://stackoverflow.com/questions/9371378/warning-not-found-favicon-ico (minor error I had)


# ===========================================================================================================================
# Python abstract classes and inheritance related refs:

    # Abstract class: 
        # Made to be inherited from instead of being used directly, and so prevents creating an object of itself. 
        # It also obliges to override its @abstractmethod(s) in its child classes.
    # https://stackoverflow.com/questions/40834145/whats-the-point-of-staticmethod-in-python :
        # * instance methods: require the instance as the first argument
        # * class methods: require the class as the first argument
        # * static methods: require neither as the first argument   
    # https://www.youtube.com/watch?v=TeDlx2Klij0 
    # https://towardsdatascience.com/how-to-use-abstract-classes-in-python-d4d2ddc02e90
    # https://www.youtube.com/watch?v=xUxbEy4WSy0 - @property (Let's you use a function like a regular attribute, IOW without '()'.)


# ===========================================================================================================================
#  token refs:

    # (The main difference between the session and token authentication is that the authentication details are stored on the server side 
    # in session authentication, and on the user side in token authentication.)

    # (Auth properties to determine if the incoming request should be permitted. Permissions are used to grant or deny access different
    #  classes of users to different parts of the API.)

    # https://blog.devgenius.io/token-authentication-in-django-rest-framework-9e6a7f97efa0
    # https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html
    # Django Rest Framework Authentication 🔒 ✅ Scalable Auth in 27 minutes [2023] : https://www.youtube.com/watch?v=llrIu4Qsl7c
    # https://docs.djangoproject.com/en/4.2/topics/auth/default/#permissions-and-authorization
    # User Role Based Permissions & Authentication | Django (3.0) Crash Course Tutorials (pt 15) : https://www.youtube.com/watch?v=eBsc65jTKvwhttps://www.youtube.com/watch?v=eBsc65jTKvw
    # https://stackoverflow.com/questions/44212188/get-user-object-from-token-string-in-drf
    # https://stackoverflow.com/questions/31813572/access-token-from-view?rq=3


# ===========================================================================================================================
# mixin refs:

    # https://stackoverflow.com/questions/860245/mixin-vs-inheritance#:~:text=With%20multiple%20inheritance%2C%20new%20class,a%20variety%20of%20parent%20classes.


# ===========================================================================================================================
# test refs:

    # https://stackoverflow.com/questions/55175709/django-channels-pytest-testing-django-core-exceptions-improperlyconfigured
    # https://docs.pytest.org/en/7.1.x/how-to/unittest.html
    # https://docs.pytest.org/en/7.3.x/how-to/skipping.html

    # basic commands:
        # pytest           --> runs all tests
        # pytest -x        --> stops running once a test fails
        # pytest -m "some_marker"  --> runs only the tests that have the specified marker [here are some useful built-in markers: @pytest.mark.skip, @pytest.mark.xfail]
        # pytest .\app\tests\test_file.py::test_x  --> runs only the specified test
        # pytest .\app\tests\test_file.py          --> runs all the tests within the specified file

    # quick example:
        # def test_good_example():
        #     assert 1 == 1

        # # @pytest.mark.xfail
        # def test_bad_example():
        #     assert 1 == 2

    # https://pytest-django.readthedocs.io/en/latest/tutorial.html
    # https://www.youtube.com/playlist?list=PLOLrQ9Pn6caw3ilqDR8_qezp76QuEOlHY
    # https://stackoverflow.com/questions/21458387/transactionmanagementerror-you-cant-execute-queries-until-the-end-of-the-atom
    # https://stackoverflow.com/questions/34466027/in-pytest-what-is-the-use-of-conftest-py-files
    # https://pytest-django.readthedocs.io/en/latest/database.html
    # https://docs.pytest.org/en/stable/explanation/fixtures.html
    # https://docs.python.org/3/library/unittest.html#test-cases
    # https://stackoverflow.com/questions/4532681/how-to-remove-all-of-the-data-in-a-table-using-django #for tearDown() if you'll end up using fixtures and setUp()
    # https://stackoverflow.com/questions/9539441/run-python-django-management-command-from-a-unittest-webtest + https://docs.djangoproject.com/en/2.0/ref/django-admin/#django.core.management.call_command
    # https://stackoverflow.com/questions/51783757/pytest-scopemismatch-error-how-to-use-fixtures-properly
    # https://stackoverflow.com/questions/59045200/proper-way-to-return-mocked-object-using-pytest-fixture
    # https://stackoverflow.com/questions/26298821/django-testing-model-with-imagefield
    # https://docs.djangoproject.com/en/dev/topics/http/sessions/
    # https://docs.djangoproject.com/en/4.2/topics/http/sessions/
    # https://stackoverflow.com/questions/31633259/django-how-to-use-decorator-in-class-based-view-methods
    # https://stackoverflow.com/questions/55668375/object-of-type-authtoken-is-not-json-serializable


# ===========================================================================================================================
# API & serializer refs:

    # ModelViewSet: 
        # [The ModelViewSet class inherits from GenericAPIView and includes implementations for various actions, 
        # by mixing in the behavior of the various mixin classes. The actions provided by the ModelViewSet class are: .list() , 
        # .retrieve() , .create() , .update() , .partial_update() , and .destroy().]
    # https://www.django-rest-framework.org/api-guide/viewsets/
    # https://drf-spectacular.readthedocs.io/en/latest/readme.html
    # https://rohitkrgupta.medium.com/swagger-with-django-made-easy-a-drf-spectacular-explainer-20b18bb4c33c
    #  Django REST Framework Oversimplified : https://www.youtube.com/watch?v=cJveiktaOSQ
    #  Django DRF Project | API Documentation with Swagger UI | 18 : https://www.youtube.com/watch?v=XBxssKYf5G0
    # https://opensource.com/article/20/11/django-rest-framework-serializers
    # https://testdriven.io/tips/97912c77-ce83-4599-812b-857ada7452ed/
    # https://testdriven.io/blog/drf-serializers/#custom-data-validation
    # https://stackoverflow.com/questions/67521669/using-filefield-imagefield-with-swagger-ui-and-drf-spectacular
    # https://stackoverflow.com/questions/61546030/how-to-encrypt-password-before-saving-it-to-user-model-django
    # https://stackoverflow.com/questions/22616973/django-rest-framework-use-different-serializers-in-the-same-modelviewset
    # https://stackoverflow.com/questions/41110742/django-rest-framework-partial-update
    # https://stackoverflow.com/questions/70123477/is-there-a-way-to-allow-blank-data-for-django-restframework
    # https://stackoverflow.com/questions/65168463/how-to-know-action-http-method-type-in-drf-generic-views
    # https://stackoverflow.com/questions/45532965/django-rest-framework-serializer-without-a-model
    # https://stackoverflow.com/questions/9549867/django-rest-framework-limit-the-allowed-methods-to-get?rq=3
    # https://www.django-rest-framework.org/api-guide/views/
    # https://stackoverflow.com/questions/41379654/difference-between-apiview-class-and-viewsets-class?rq=3
    # https://stackoverflow.com/questions/54702823/difference-between-viewset-and-genericviewset-in-django-rest-framework
    # https://www.django-rest-framework.org/api-guide/viewsets/
    # https://stackoverflow.com/questions/75835705/how-to-show-required-request-body-using-django-rest-framework-drf-spectacular
    # https://www.django-rest-framework.org/api-guide/authentication/
    # https://stackoverflow.com/questions/26639169/csrf-failed-csrf-token-missing-or-incorrect
    # https://stackoverflow.com/questions/68181833/detail-csrf-failed-csrf-token-missing-or-incorrect-django-rest-framework
    # https://stackoverflow.com/questions/30871033/django-rest-framework-remove-csrf
    # https://stackoverflow.com/questions/61043353/django-rest-framework-detail-authentication-credentials-were-not-provided
    # https://stackoverflow.com/questions/33400830/restrict-update-method-to-only-modify-request-users-own-data
    # https://www.django-rest-framework.org/api-guide/authentication/
    # The list of HTTP method names that this view will accept: ["get", "post", "put", "patch", "delete", "head", "options", "trace"] --> https://docs.djangoproject.com/en/4.2/ref/class-based-views/base/
    # A viewset that provides default `create()`, `retrieve()`, `update()`, `partial_update()`, `destroy()` and `list()` actions.
    # https://stackoverflow.com/questions/23639113/disable-a-method-in-a-viewset-django-rest-framework
    # https://stackoverflow.com/questions/22988878/pass-extra-arguments-to-serializer-class-in-django-rest-framework
    # https://stackoverflow.com/questions/6382806/django-save-update-on-duplicate-key
    # https://stackoverflow.com/questions/14832115/get-the-last-inserted-id-in-django
    # https://stackoverflow.com/questions/47698836/integrityerror-1451-cannot-delete-or-update-a-parent-row-a-foreign-key-cons


# ===========================================================================================================================
# React:

    # https://www.guvi.in/blog/how-to-fetch-data-using-api-in-react/
    # https://blog.logrocket.com/using-react-django-create-app-tutorial/
    # React + Django Integration Tutorial | Hello World App : https://www.youtube.com/watch?v=F9o4GSkSo40
    # Connect Django Backend to React.js Frontend - Full Stack App Development Tutorial : https://www.youtube.com/watch?v=fBA-jaWab9k
    # https://stackoverflow.com/questions/64119725/create-react-app-build-does-not-work-correctly
    # https://stackoverflow.com/questions/67962030/warning-adding-embedded-git-repository-when-adding-a-new-create-react-app-fol
    # https://stackoverflow.com/questions/17628305/windows-git-warning-lf-will-be-replaced-by-crlf-is-that-warning-tail-backwar
    # https://github.com/trendmicro-frontend/react-sidenav
    # https://stackoverflow.com/questions/65770679/encountering-white-space-at-top-of-react-app
    # https://www.codevertiser.com/reactjs-responsive-navbar/
    # https://stackoverflow.com/questions/67847249/how-to-keep-user-logged-in-in-react-app-with-a-django-back-end
    # Building a user authentication app with React and Django Rest Framework : https://www.youtube.com/watch?v=diB38AvVkHw + https://github.com/dotja/authentication_app_react_django_rest
    # https://react-bootstrap.netlify.app/docs/forms/form-control
    # https://stackoverflow.com/questions/55339291/axios-catch-error-request-failed-with-status-code-404
    # https://stackoverflow.com/questions/74164058/is-it-necessary-to-check-if-axios-response-status-is-200-or-not
    # https://stackoverflow.com/questions/49967779/axios-handling-errors
    # https://stackoverflow.com/questions/48298890/axios-how-to-get-error-response-even-when-api-return-404-error-in-try-catch-fi
    # https://stackoverflow.com/questions/61028344/axios-post-method-there-is-error-error-request-failed-with-status-code-405
    # https://stackoverflow.com/questions/46337471/how-to-allow-cors-in-react-js
    # https://stackoverflow.com/questions/35760943/how-can-i-enable-cors-on-django-rest-framework
    # https://stackoverflow.com/questions/67327660/cors-not-working-in-django-but-settings-seem-correct
    # https://stackoverflow.com/questions/40052918/how-to-get-the-file-data-from-a-react-bootstrap-formcontrol-component
    # https://stackoverflow.com/questions/43013858/how-to-post-a-file-from-a-form-with-axios
    # https://stackoverflow.com/questions/71031271/not-getting-image-file-in-nodejs-after-posting-from-react
    # https://saificode.blogspot.com/2022/08/image-upload-in-react-js-how-to-upload.html
    # https://stackoverflow.com/questions/69611485/react-to-django-cors-issue
    # https://stackoverflow.com/questions/44037474/cors-error-while-consuming-calling-rest-api-with-react?noredirect=1&lq=1
    # https://stackoverflow.com/questions/74164058/is-it-necessary-to-check-if-axios-response-status-is-200-or-not
    # https://stackoverflow.com/questions/40477245/is-it-possible-to-use-if-else-statement-in-react-render-function
    # https://stackoverflow.com/questions/32500073/request-header-field-access-control-allow-headers-is-not-allowed-by-itself-in-pr
    # React Sidebar Navigation Menu using React Router v6.4 - Beginner Tutorial : https://www.youtube.com/watch?v=zQBd3hNXJgI + https://github.com/briancodex/react-sidebar-router-v6.4/blob/main/src/routes/Products.js
    # https://stackoverflow.com/questions/73593938/is-there-any-way-in-css-to-make-other-objects-move-when-another-object-is-scaled
    # 42 ReactJS basics - show images from API : https://www.youtube.com/watch?v=esFJqNnhp8U
    # https://stackoverflow.com/questions/65080448/how-to-display-all-items-from-an-api-in-react-js
    # https://www.codingthesmartway.com/how-to-fetch-api-data-with-react/
    # https://stackoverflow.com/questions/44969877/if-condition-inside-of-map-react?rq=3
    # https://stackoverflow.com/questions/39523040/concatenating-variables-and-strings-in-react
    # https://stackoverflow.com/questions/63255557/fetch-data-from-multiple-pages-of-an-api-in-react-native
    # https://stackoverflow.com/questions/53090699/how-to-run-an-alert-on-button-click-react-js
    # https://stackoverflow.com/questions/14705245/static-url-path-setting-in-django
    # https://stackoverflow.com/questions/6014663/django-static-file-not-found
    # https://stackoverflow.com/questions/67142135/cant-display-an-image-in-react-from-backend-django
    # https://stackoverflow.com/questions/70890133/image-is-not-loading-from-django-rest-framework-in-react
    # https://stackoverflow.com/questions/73678855/fetch-and-display-image-from-api-react
    # https://stackoverflow.com/questions/31785966/django-rest-framework-turn-on-pagination-on-a-viewset-like-modelviewset-pagina
    # https://stackoverflow.com/questions/42089548/how-to-add-delay-in-react-js
    # https://stackoverflow.com/questions/40029867/trying-to-implement-a-simple-promise-in-reactjs
    # https://stackoverflow.com/questions/38731271/clear-an-input-field-with-reactjs
    # https://stackoverflow.com/questions/69233210/how-to-conditional-disable-input-depend-on-another-input-value-in-react-hook-fo?rq=3
    # https://stackoverflow.com/questions/65583610/in-react-how-to-convert-utc-datetime-to-more-readable-string-inside-the-table
    # https://stackoverflow.com/questions/71960194/update-navbar-after-success-login-or-logout-redirection
    # https://stackoverflow.com/questions/237104/how-do-i-check-if-an-array-includes-a-value-in-javascript?noredirect=1&lq=1
    # https://stackoverflow.com/questions/71663858/nested-ternary-operator-for-react-components
    # https://stackoverflow.com/questions/70756777/react-reload-page-only-once-if-variable-changes
    # https://stackoverflow.com/questions/74428905/after-login-i-want-to-refresh-the-navbar-is-rendering-only-when-i-refresh-the-p
    # https://stackoverflow.com/questions/73218944/how-to-refresh-page-with-react-router
    # https://stackoverflow.com/questions/71960194/update-navbar-after-success-login-or-logout-redirection
    # Redux Tutorial (with Redux Toolkit) : https://www.youtube.com/watch?v=iBUJVy8phqw
    # https://redux-toolkit.js.org/tutorials/quick-start
    # https://stackoverflow.com/questions/62966863/a-case-reducer-on-a-non-draftable-value-must-not-return-undefined
    # https://stackoverflow.com/questions/64237538/strange-behviour-of-state-in-slice-redux-toolkit-revoked-proxy
    # https://stackoverflow.com/questions/56502838/is-it-ok-to-make-a-rest-api-request-from-within-a-redux-reducer
    # Redux Toolkit Tutorial - 30 - Fetching Data : https://www.youtube.com/watch?v=I2aM7YcOXDY
    # React Redux Toolkit Setup and CreateAsyncThunk on API : https://www.youtube.com/watch?v=Oc14xbizA2o
    # https://stackoverflow.com/questions/41964204/react-redux-store-updating-but-component-not-re-rendering
    # Create a Table in React | Learn how to view, add, delete and edit rows in a table from Scratch : https://www.youtube.com/watch?v=dYjdzpZv5yc
    # https://stackoverflow.com/questions/42352941/how-to-send-input-hidden-in-react-js
    # https://stackoverflow.com/questions/5765398/whats-the-best-way-to-convert-a-number-to-a-string-in-javascript
    # https://stackoverflow.com/questions/41610811/react-js-how-to-send-a-multipart-form-data-to-server
    # https://stackoverflow.com/questions/58116211/how-to-redirect-to-another-page-on-button-click-in-reactjs
    # https://stackoverflow.com/questions/56769076/how-to-show-base64-image-in-react
    # https://dev.to/salehmubashar/search-bar-in-react-js-545l


# ===========================================================================================================================
# Random Data Generation:

    # https://pynative.com/python-random-randrange/
    # https://renatobudinich.com/create-random-images-with-randimage/
    # https://stackoverflow.com/questions/902761/saving-a-numpy-array-as-an-image
    # https://stackoverflow.com/questions/47290668/image-fromarray-just-produces-black-image
    # https://pypi.org/project/randimage/
    # https://pypi.org/project/names/   
    # https://pypi.org/project/random-address/
    # https://github.com/tolstislon/phone-gen
    # https://github.com/eye9poob/python/blob/master/credit-card-numbers-generator.py
    # https://pypi.org/project/randominfo/
    # https://pypi.org/project/random-username/
    # https://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates

# ===========================================================================================================================
# JavaScript:

    #

# ===========================================================================================================================
# CSS, HTML:

    # https://stackoverflow.com/questions/28057933/hiding-button-after-collapse-is-toggled-in-bootstrap
    # https://stackoverflow.com/questions/787839/resize-image-proportionally-with-css
    # https://stackoverflow.com/questions/2570972/css-font-border
    # https://developer.mozilla.org/en-US/docs/Web/CSS/text-shadow
    # https://stackoverflow.com/questions/35990445/how-to-move-a-div-up-and-down-infinitely-in-css3
    # https://stackoverflow.com/questions/12132884/how-to-define-multiple-classes-hover-event-in-css
    # https://stackoverflow.com/questions/11807286/how-to-make-div-background-color-transparent-in-css
    # https://stackoverflow.com/questions/68674228/css-width-fit-content-cancels-text-align-center
    # https://codepen.io/palimadra/pen/OVvbaY
    # https://stackoverflow.com/questions/38918453/i-need-to-center-the-div-in-td
    # https://stackoverflow.com/questions/1895476/how-do-i-style-a-select-dropdown-with-only-css
    # https://stackoverflow.com/questions/38442702/getting-rid-of-yellow-fill-on-input-after-email-auto-fill-from-chrome
    # https://stackoverflow.com/questions/25685227/how-to-display-user-profile-image-in-circle


# ===========================================================================================================================
# Deployment:

    # https://stackoverflow.com/questions/65431326/django-app-on-azure-not-getting-static-files
    # https://stackoverflow.com/questions/66821626/django-doesnt-load-build-static-files-reactjs
    # https://www.atatus.com/blog/host-react-app-for-free/#firebase
    # https://stackoverflow.com/questions/72236942/react-application-built-on-top-of-firebase-renders-404-on-page-refresh
    # https://stackoverflow.com/questions/46235798/relative-path-in-index-html-after-build
    # https://stackoverflow.com/questions/62992831/python-session-samesite-none-not-being-set
    # https://stackoverflow.com/questions/45122296/firebase-pass-url-param-in-url-rewrite

# ===========================================================================================================================
# Docker:

    # https://www.freecodecamp.org/news/how-to-dockerize-a-react-application/
    # docker image build -t ars-web:latest .
    # docker run -dp 8000:3000 --name react-example-container ars-web:latest


# ===========================================================================================================================
# general:

    # https://stackoverflow.com/questions/115983/how-do-i-add-an-empty-directory-to-a-git-repository
    # https://stackoverflow.com/questions/4406501/change-the-name-of-a-key-in-dictionary
    # https://stackoverflow.com/questions/13349573/how-to-change-a-django-querydict-to-python-dict
    # https://stackoverflow.com/questions/6340794/yyyy-mm-ddthhmmss-what-is-the-meaning-of-t-here
    # https://stackoverflow.com/questions/17508027/cant-access-cookies-from-document-cookie-in-js-but-browser-shows-cookies-exist
    # https://stackoverflow.com/questions/12164453/how-to-store-objects-in-back-end-sessions-in-django-just-like-django-stores-user


