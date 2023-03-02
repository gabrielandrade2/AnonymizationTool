class Type(Enum):
    '医師記録',
    '看護師記録',
    '_2018年以前'

def loadDoctorRecords(f):
    sheet = f.parse(Type.医師記録.value)
    texts = [sheet['SUBJETIVE'].to_list()]


def loadNursingRecords(f):
    pass


def loadDocsBefore2018(f):
    pass


def load_texts(file, type:Type):
    with pd.ExcelFile(file) as f:
        if type == Type.医師記録:
            return loadDoctorRecords(f)
        elif type == Type.看護師記録:
            return loadNursingRecords(f)
        elif type == Type._2018年以前:
            return loadDocsBefore2018(f)
        else:
            raise Exception('Unknown type')