from pydantic import BaseModel

class IdExtractor(BaseModel):
    job_title_element = 'li'
    job_title_element_class = 'result-card job-result-card result-card--with-hover-state'
    job_id_element_identifier = 'data-id'

class ExtractorJobElement(BaseModel):
    name: str
    element: str
    element_class: str
    attribute_name: str
    alt_element_class: str = ''
    inner_element: str = ''
    inner_inner_element: str = ''
    inner_inner_inner_element: str = ''

class DataExtractor(BaseModel):
    job_data: list = [
        ExtractorJobElement(
            name= 'job_title',
            element= 'h2',
            element_class= 'topcard__title',
            attribute_name= 'class'
        ),
        ExtractorJobElement(
            name= 'description',
            element= 'section',
            element_class= 'description',
            attribute_name= 'class'

        ),
        ExtractorJobElement(
            name= 'location',
            element= 'span',
            element_class= 'topcard__flavor topcard__flavor--bullet',
            attribute_name= 'class'

        ),
          ExtractorJobElement(
            name= 'n_applicants',
            element= 'span',
            element_class= 'topcard__flavor--metadata topcard__flavor--bullet num-applicants__caption',
            attribute_name= 'class'

        ),
          ExtractorJobElement(
            name= 'date_posted',
            element= 'span',
            element_class= 'topcard__flavor--metadata posted-time-ago__text',
            alt_element_class= 'topcard__flavor--metadata posted-time-ago__text posted-time-ago__text--new',
            attribute_name= 'class'

        ),
         ExtractorJobElement(
            name= 'employer',
            element= 'a',
            element_class= 'topcard__org-name-link topcard__flavor--black-link',
            attribute_name= 'class'

        )

    ]
    job_meta: ExtractorJobElement = ExtractorJobElement(
        name= 'job_title',
        element= 'ul',
        element_class= 'job-criteria__list',
        attribute_name= 'class',
        inner_element= 'li',
        inner_inner_element= 'h3',
        inner_inner_inner_element='span'
    )

