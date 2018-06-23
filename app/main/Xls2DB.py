#from openpyxl import  load_workbook
#from .. import db
#from ..models import Scripture, Chapter, Section, Sentence, Reader, RecentList
#
#
#def  save( file ):
#    print "process file" + str(file)
#    data = load_workbook(file)
#    print data
#    sheet = data.get_sheet_by_name("Sheet1")
#
#    scripture = None
#    chapter = None
#    section = None
#
#    for row in xrange( 2, 10000000):
#        title =  unicode(sheet.cell( row=row, column=2).value)
#        origin = sheet.cell( row=row, column=4).value
#        modern = sheet.cell( row=row, column=5).value
#        annotation = sheet.cell( row=row, column=6).value
#
#        if "None" == title:
#            break
#
#        fields = title.split(u'-')
#
#        if not scripture :
#            scripture = Scripture( scripture_display=fields[0], scripture_title=fields[0])
#            db.session.add( scripture )
#            db.session.flush()
#
#            chapter = Chapter(scripture_id=scripture.id, chapter_display="None", chapter__title="None")
#            db.session.add( chapter)
#            db.session.flush()
#
#            scripture.chapters = []
#            scripture.chapters.append( chapter )
#
#
#        if not section:
#            section = Section(chapter_id=chapter.id, section_display=fields[1], section__title=fields[1])
#            db.session.add(section)
#            db.session.flush()
#
#            chapter.sections = []
#            chapter.sections.append(section)
#        else :
#            if section.section_display == fields[1]:
#                pass
#            else:
#                section = Section(chapter_id=chapter.id, section_display=fields[1], section__title=fields[1])
#                db.session.add(section)
#                db.session.flush()
#
#                chapter.sections.append(section)
#
#        sentence = Sentence(scripture_id=scripture.id, chapter_id=chapter.id, section_id=section.id, classic_text=origin, modern_text=modern, annotation_text=annotation)
#        db.session.add(sentence)
#        db.session.flush()
#
#        if not section.sentences:
#            section.sentences = []
#
#        section.sentences.append(sentence)
#
#    db.session.commit()
#
#
#
#
