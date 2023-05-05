import os
import random
import shutil
from summarisers import *
import codecs

download_folder = "..\samplepdfs"
destination_folder = os.path.dirname(os.path.abspath(__file__)) + "\\testcorpus"

def get_test_corpus():
    theses_topics = []
    theses_with_topic = []
    chosen_theses = []
    for filename in os.listdir(download_folder):
        topic = (filename.split("-")[1]).split(".")[0]
        if topic not in theses_topics:
            theses_topics.append(topic)
            theses_with_topic.append([filename])
        else:
            theses_with_topic[theses_topics.index(topic)].append(filename)
    for topic in theses_topics:
        chosen_thesis = random.choice(theses_with_topic[theses_topics.index(topic)])
        shutil.copyfile(download_folder + "\\" + chosen_thesis, destination_folder + "\\" + chosen_thesis)
    for filename in os.listdir(destination_folder):
        os.rename(destination_folder + "\\" + filename, destination_folder + "\\" + filename.split("-")[1])

def verify_validity_of_corpus():
    counter = 0
    for topic in theses_topics:
        print(topic)
        print(len(theses_with_topic[theses_topics.index(topic)]))
        counter += len(theses_with_topic[theses_topics.index(topic)])
    print(counter)

def test_methods_on_abstracts():
    incomplete = []
    for abstract in os.listdir(destination_folder + "\\abstracts"):
        real_abstract = open(destination_folder + "\\abstracts" + "\\" + abstract, "r").read()
        open("abstractsummaryscores.txt", "a").write(str(abstract) + "\n")
        print(str(abstract) + ": Legacy")
        # Legacy Method
        legacy = legacy_summariser(real_abstract, 250)
        open("abstractsummaryscores.txt", "a").write("Legacy: " + str(calculateMetrics(real_abstract, legacy)) + "\n")
        print(str(abstract) + ": LEDBase")
        # New Method 1
        ledbase16384 = new_summariser(real_abstract, "allenai/led-base-16384")
        open("abstractsummaryscores.txt", "a").write("Base: " + str(calculateMetrics(real_abstract, ledbase16384)) + "\n")
        print(str(abstract) + ": LEDLarge")
        # New Method 2
        ledlarge16384 = new_summariser(real_abstract, "allenai/led-large-16384")
        open("abstractsummaryscores.txt", "a").write("Large: " + str(calculateMetrics(real_abstract, ledlarge16384)) + "\n")
        print(str(abstract) + ": LEDLargeArxiv")
        # New Method 3
        ledarxiv16384 = new_summariser(real_abstract, "allenai/led-large-16384-arxiv")
        open("abstractsummaryscores.txt", "a").write("Arxiv: " + str(calculateMetrics(real_abstract, ledarxiv16384)) + "\n")
        print(str(abstract) + ": LEDLargePubmed")
        # New Method 4
        ledpubmed16384 = new_summariser(real_abstract, "patrickvonplaten/led-large-16384-pubmed")
        open("abstractsummaryscores.txt", "a").write("Pubmed: " + str(calculateMetrics(real_abstract, ledpubmed16384)) + "\n")
        # New Method 5
        leddialog16384 = new_summariser(real_abstract, "MingZhong/DialogLED-base-16384")
        open("abstractsummaryscores.txt", "a").write("Dialog: " + str(calculateMetrics(real_abstract, leddialog16384)) + "\n")
        # New Method 6
        ledbooklarge16384 = new_summariser(real_abstract, "pszemraj/led-large-book-summary")
        open("abstractsummaryscores.txt", "a").write("largebook: " + str(calculateMetrics(real_abstract, ledbooklarge16384)) + "\n")
        # New Method 7
        ledbookbase16384 = new_summariser(real_abstract, "pszemraj/led-base-book-summary")
        open("abstractsummaryscores.txt", "a").write("basebook: " + str(calculateMetrics(real_abstract, ledbookbase16384)) + "\n")
        # # New Method 8
        ledlegal16384 = new_summariser(real_abstract, "nsi319/legal-led-base-16384")
        open("abstractsummaryscores.txt", "a").write("legal: " + str(calculateMetrics(real_abstract, ledlegal16384)) + "\n")

def compare_chapters():
    abstract = open(destination_folder + "\\chapteranalysis\\" + "abstract.txt", "r").read()
    chapters = os.listdir(destination_folder + "\\chapteranalysis")
    for chapter in chapters:
        for chapter2 in chapters:
            if chapter == chapter2:
                continue
            else:
                chapterfile = open(destination_folder + "\\chapteranalysis\\" + chapter, "r").read()
                chapter2file = open(destination_folder + "\\chapteranalysis\\" + chapter2, "r").read()
                open("chapterscores.txt", "a").write(chapter + chapter2 + ": " + str(calculateMetrics(abstract, chapterfile+chapter2file)) + "\n")

# def compare_summarisation_methods():
#     #for i in range(1,4):
#         #if (i == 1) or (i == 3):
#             #continue
#         #open("introconclsummaryscores.txt", "a").write(str(i) + "\n")
#     abstract = open(destination_folder + "\\" + str(1) +"\\" + "abstract.txt", "r").read().strip("\n")
#     introduction = open(destination_folder + "\\" + str(1) +"\\" + "intro.txt", "r").read().strip()
#     conclusion = open(destination_folder + "\\" + str(1) +"\\" + "concl.txt", "r").read().strip("\n")
#         #print(batches(introduction))
#         # print("Introduction")
#         # print(introduction)
#         # print("Conclusion")
#         # print(conclusion)

#     introduction = legacy_summariser(introduction.replace("  ", " "), 5000)
#     conclusion = legacy_summariser(conclusion.replace("  ", " "), 5000)

#         #print(legacy_summariser(introduction, 5000))
#         #print(new_summariser(introduction, "allenai/led-base-16384"))
#         #print(new_summariser(intro_summary, "allenai/led-large-16384"))

#     summarisebothsummariestogether = combined_summarisation(introduction, conclusion)
#     print(summarisebothsummariestogether)
        # open("introconclsummaryscores.txt", "a").write(str(calculateMetrics(abstract, summarisebothsummariestogether)) + "\n")
        # summarisebothsummariesseperately = combined_summarisation2(introduction, conclusion)
        # open("introconclsummaryscores.txt", "a").write(str(calculateMetrics(abstract, summarisebothsummariesseperately)) + "\n")
        # summarisebothsummariesseperate1 = combined_summarisation_seperate(introduction, conclusion)
        # open("introconclsummaryscores.txt", "a").write(str(calculateMetrics(abstract, summarisebothsummariesseperate1)) + "\n")
        # summarisebothsummariesseperate2 = combined_summarisation_seperate(conclusion, introduction)
        # open("introconclsummaryscores.txt", "a").write(str(calculateMetrics(abstract, summarisebothsummariesseperate2)) + "\n")
        # summarisebothsummariesaddition = combined_summarisation_seperate(introduction+conclusion, "")
        # open("introconclsummaryscores.txt", "a").write(str(calculateMetrics(abstract, summarisebothsummariesaddition)) + "\n")
        # open("introconclsummaryscores.txt", "a").write(summarisebothsummariestogether + "\n")

#compare_summarisation_methods()

text1 = "To achieve these competencies, nursing students must apply both knowledge and skills based on current and best available evidence that is indicative of safe nursing practice. This has developed over a number of years through my professional experience as a nurse academic and my subsequent contact with nursing students who have dyslexia within higher education (HE). This studyâ€™s findings revealed the multiple and varied difficulties dyslexic nursing students experience in clinical placement, along with evidence of a lack of understanding about dyslexia from some nurse mentors. However, this study did not explore in any depth the nurse mentorâ€™s perceptions of dyslexia and a number of questions remained unanswered; specifically, what happens once a nursing student with dyslexia becomes a registered nurse and is the question of safety truly a justifiable issue of concern surrounding a nurse with dyslexia? The research surrounding dyslexia and nursing to date has explored, for the most part, dyslexia amongst nursing students (Evans 2014b). Therefore, my study aims to present a unique insight into a dyslexic nursing studentâ€™s journey from nursing student to registered nurse including those who guide and support them through this academic and clinical journey. Chapter 3 presents a systematic literature review of nursing and dyslexia. This research collectively identified a range of difficulties that nursing students in clinical practice face including difficulty in spelling, retaining information and writing nursing reports, for example. Additionally, a number of these studies identified evidence of negative attitudes from nursing colleagues and mentors towards nursing students with dyslexia (Price & Gale 2006; Sanderson-Mann & McCandless 2005; Morris & Turnbull 2006; White 2007; Child & Langford 2011; Ridley 2011; Sanderson-Mann et al. This research collectively identified a range of difficulties that nursing students in clinical practice face including difficulty in spelling, retaining information and writing nursing reports. Additionally, a number of these studies identified evidence of negative attitudes from nursing colleagues and mentors towards nursing students with dyslexia (Price & Gale 2006; Sanderson-Mann & McCandless 2005; Morris & Turnbull 2006; White 2007; Child & Langford 2011; Ridley 2011; Sanderson-Mann et al. This research collectively identified a range of difficulties that nursing students in clinical practice face including difficulty in spelling, retaining information and writing nursing reports, for example. Additionally, a number of these studies identified evidence of negative attitudes from nursing colleagues and mentors towards nursing students with dyslexia (Price & Gale 2006; Morris & Turnbull 2006; White 2007; Ridley 2011; Evans 2014a). Some of these studies also highlighted an unwillingness to disclose dyslexia amongst nursing students for fear of a negative reaction and being seen in a less positive light (Morris & Turnbull 2007a; White 2007; Sanderson-Mann & McCandless 2005; Ridley 2011; Evans 2014a)."
abstract1 = "Aim:  This  longitudinal  study  explores  the  experiences  of  six  nursing  students  who have dyslexia in the final six months of their nursing course, revisiting them in their first six months as registered nurses. Additionally, the study explores the experiences of those who support them through this transition from student nurse to registered nurse: their tutors at university, and their mentors and preceptors in practice. Background: Current and past literature exploring the nursing student with dyslexia reveals many have  either  negative or  positive experiences in clinical practice, influenced through the perceptions of others. Additionally, it highlights they experience a variety of difficulties in practice, but many have adopted compensatory strategies to overcome these. There is also evidence of varied levels of understanding of dyslexia, as  well  as  levels  of  support,  from  mentors,  with  evidence  of  judgmental  attitudes towards  nursing  students  with  dyslexia.  There  is  limited  research  surrounding  the experiences of registered nurses with dyslexia in practice.  Design: A longitudinal interpretative case study design was adopted for this study. Six nursing students with dyslexia in the final six months of their undergraduate nursing course  were  recruited.  The  study  revisited  them  within  their  first  six  months  as registered nurses. The mentors, tutors and preceptors had a direct connection to the student nurses, supporting them either at university or in practice. All participants were interviewed with iterative semi-structured interviews using interpretative phenomenological analysis to analyse the interview data.  Results: The students showed degrees of negative self-perceptions, some carried these forward as registered nurses. Some of the mentors, tutors and preceptors lacked knowledge  and  understanding  of  dyslexia,  with  some  expressing  concerns  over  the safety of a nurse with dyslexia in practice. Conclusion:  The  study  provides  evidence  of  a  dyslexic  self-stigma  and  fear  of others' perceptions surrounding dyslexia, but also full acceptance of dyslexia amongst some  nurse  participants.  Dyslexia  is  perceived  differently,  with  evidence  of  positive understanding,  but  also  that  dyslexia  is  misunderstood  and  linked  to  concerns surrounding patient safety in nursing practice.".replace("  ", " ")
text2 = "Human rights is a relatively new subject in international law. Yet, the striving for certain human rights, and for civil liberties against tyrannical and oppressive regimes, is old as time itself. The concept that all human beings must enjoy certain fundamental rights emerged from the traditional international law concerning states' responsibility for injuries to aliens.' However, the state's treatment of its own nationals was considered to be a matter strictly within the state's domestic jurisdiction and totally outside international concern. A few notable exceptions have been the abolition of the slave trade on the high seas in the early nineteenth century, the international concern over massacres of Armenians in the Ottoman Empire in the early twentieth century, and the International Convention on the Elimination of All Forms of Intolerance and Discrimination Based on Religion or Belief in the early twentieth century. The International Convention on the Protection of the Rights of the Minorities in the early twentieth century. The International Convention on the Protection of the Rights of the Minorities in the early twentieth century. The International Convention on the Protection of the Rights of the Minorities in the early twentieth century. The International Convention on the Protection of the Rights of the Minorities (1956) and the International Convention on the Elimination of All Forms of Intolerance and Discrimination Based on Religion or Belief (1981). Chapter 6: The background to the existing national and international instruments providing for free and compulsory education is related, and the writer criticises some of the instruments, examining Article 2 of the First Protocol to the European Convention in particular. The writer looks at the  United Nations  Instruments,  including the Supplementary Convention on the Abolition of Slavery, and the Slave Trade, and Institutions and Practices Similar to Slavery (1956), and describes the role and achievements of the International Labour Organisation. The writer examines in particular the Travaux Preparatoire of the Civil and Political Covenant and the findings of Working Group 1 of the Siracusa Conference on the Article 4 derogation provision, and argues that the Universal Declaration, and the Economic, Social and Cultural Covenant contained no derogation clauses, and there is no derogation form the right to education. The writer examines the International Covenant on Civil and Political Rights (1948) and the two International Covenants on Human Rights (1966); the Covenant on Economic, Social and Cultural Rights. Moreover, several instruments protecting and promoting human rights have been adopted under the auspices of the Specialised Agencies of the United Nations. Thus, whereas the body of law on stateresponsibility is enunciated alongside other internationally recognised basic human rights such as the right to life, the right not be tortured or inhumanly treated or punished and the right not to be held in slavery or servitude. The second assertion was that the right to free and compulsory primary education has become a legally binding rule of customary international law.  This submission rests on the premise that the United Nations Declaration of Human Rights (1948), is now ranked as a binding norm of customary international law. Customary international law, as defined in Article 38(1)(b) of the Statute of the International Court of Justice, is 'a general practice accepted as a law.' The importance of customary international law, as a source of customary international law."
abstract2 = "Today education is seen as a fundamental human right since it is a prerequisite for the development of the individual's intellectual and spiritual potential and is essential to the proper exercise of his other rights and duties. Through education, society transmits its norms and values; this is how the social system is reproduced. This study deals with human rights generally and with the right to education specifically. Its purpose is to prove that the right to education has become a fundamental human right which has joined the group of basic human rights and that the right to compulsory and free primary education has acquired the status of customary international law. The thesis consists of thirteen chapters, grouped into six parts.  Part one deals with the history and concept of human rights in general, and the right to education in particular. It contains Chapter 1 (Issues of Definition) and Chapter 2 (The Evolution of the Right to Education). Part Two examines the concepts of the child and the age of majority in national and international law, covering Chapter 3 (Children and their Protection in International Law) and Chapter 4 (The Child and his Age of Majority). Part Three is the core of the thesis, dealing in detail with the positive and negative legal implications of the right to education. It contains Chapter 5 to 9 inclusive, which deal respectively with the rights of parents with regard to sex and religious education, compulsory and free education, corporal punishment in schools, child labour and, finally, discrimination in education. Part Four consists of two chapters   (Derogation from and Limitation on the Right to Education), and Parts Five and Six consist of one chapter each, the former on International Remedies regarding the violation of the right to education and the latter with the writer's conclusions."

print(calculateMetrics(abstract1, text1))
print("\n")
print(calculateMetrics(abstract2, text2))