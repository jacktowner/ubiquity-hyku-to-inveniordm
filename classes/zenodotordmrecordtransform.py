#from invenio_rdm_migrator.transform.base import Transform

class ZenodoToRDMRecordTransform():
    def __init__(self, **kwargs):  # Important: Add __init__
        pass
        #super().__init__(**kwargs)  # Call parent's __init__

    def _transform(self, data):
        rdm_record = {}

        # Extract metadata
        metadata = data['metadata']

        # Map basic metadata
        rdm_record['metadata'] = {
            'title': metadata['title'],
            'resource_type': {'id': metadata['resource_type']['id']},
            'publication_date': metadata['publication_date'],
            'creators':[]
        }

        # Map creators with affiliations
        for creator in metadata['creators']:
            rdm_creator = {
                'person_or_org': {
                    'type': creator['person_or_org']['type'],
                    'name': creator['person_or_org']['name'],
                    'given_name': creator['person_or_org'].get('given_name'),
                    'family_name': creator['person_or_org'].get('family_name'),
                    'identifiers': creator['person_or_org'].get('identifiers',),
                },
                'affiliations': creator.get('affiliations',),
            }
            rdm_record['metadata']['creators'].append(rdm_creator)

        # Map parent ID (if present)
        if 'parent' in data and 'id' in data['parent']:
            rdm_record['parent'] = {'id': data['parent']['id']}

        # Add other metadata fields as needed (e.g., publisher, description)

        return rdm_record