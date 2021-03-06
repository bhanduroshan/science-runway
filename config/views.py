# -*- coding: utf-8 -*-
"""View for dashboard."""

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from .survey import load_mentor_names
from .survey import load_mentor_answers
from .survey import load_questions, load_mentor_profiles, get_mentor_match
from sciencerunaway.users.models import UserProfile, Mentors
# import json
from sciencerunaway.users.models import User
from django.template.defaulttags import register
import random
from base64 import b64encode


MAILING_LIST = "mailing_list.txt"
SURVEY_RESULTS = "survey_results.txt"

mentors = [
  {
    "Mentor Name": "carolgrieder",
    "name": "Carol Grieder",
    "Biography": "Carol Greider, Ph.D. received her bachelor¡¯s degree from the University of California at Santa Barbara in 1983 and a Ph.D. in 1987 from the University of California at Berkeley. In 1984, working together with Dr. Elizabeth Blackburn, she discovered telomerase, an enzyme that maintains telomeres, or chromosome ends.  In 1988, Dr. Greider went to Cold Spring Harbor Laboratory where, as an independent Cold Spring Harbor Fellow, she cloned and characterized the RNA component of telomerase.  In 1990, Dr. Greider was appointed as an assistant investigator at Cold Spring Harbor Laboratory, followed later by appointment to Investigator in 1994. She expanded the focus of her telomere research to include the role of telomere length in cellular senescence, cell death and in cancer.  In 1997, Dr. Greider moved her laboratory to the Department of Molecular Biology and Genetics at The Johns Hopkins University School of Medicine.  In 2003 she was appointed as the Daniel Nathans Professor and Director of the Department of Molecular Biology and Genetics.  At Johns Hopkins University, Dr. Greider¡¯s group continued to study the biochemistry of telomerase and determined the secondary structure of the human telomerase RNA. She also expanded her work to include a mouse model of dyskeratosis congenita and stem cell failure in response to short telomeres. Dr. Greider shared the Nobel Prize in Physiology or Medicine in 2009 with Drs. Elizabeth Blackburn and Jack Szostak for their work on telomeres and telomerase. Dr. Greider currently directs a group of 10 scientists studying both the role of short telomeres in age-related disease and cancer as well as the regulatory mechanism that maintain telomere length.",
    "What do you do every day?": "Days in my life are extremely varied.  I don't have a regular day- which is nice.  I will meet one on one with the researchers working in my lab and get all the nitty gritty experiment details- maybe six or seven meetings in a day, maybe once or twice a week.  I teach large lecture classes as well as small groups.  I spend time in administrative meetings- hiring and promotional meetings.  The thing I love the best is meeting one on one with scientists- or our meetings where one scientist presents their work and we all brainstorm- or our meetings based on scientific literature where we critique current articles and really learn from other's work.",
    "Why do you love it?": "There are surprising things that you learn- even little small things.  I like finding things out.  Even when you get a small thing to work, it's very satisfying!  And the big things, like RNAi for biology, that when I was a graduate student we didn't know anything about.  That's why I will be reading Science and Nature when I get home, on a Friday night.  I try to read biology generally, not just my specific field.",
    "What were your moments of fear/challenges in your career?": "One of the things I believe about science- the difference between science and politics is that in science you can always get something right- in politics you never can!  I have always prided myself on being clear that we set out to test a hypothesis, not prove a hypothesis- but I also pride myself on being correct!  There are times when we have published things that scientifically were wrong- but I felt very strongly that we had to publish the results that showed we were wrong too.  If I believe science is self correcting, it is my duty to correct myself.  There's pressure to spin things- but science doesn't move forward that way.",
    "What are some of the innovations in science that you are most excited about?": "Advances in genome sequencing- and what we can discover with the ease of genome sequencing today.  Population migration etc. that come from genetics but uses it in a very new way.",
    "Where did you grow up?": "I grew up in Davis, California- it's an academic, university town.",
    "Who was your favorite teacher and why?": "",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "When I was in junior high and high school, I used to do vaulting on horseback!  I taught horseback to six to twelve year olds as a teenager and was on a national team for it.",
    "Personal style/fashion tip? What’s in your purse?": "Be who you are- present yourself in a real way, as a real person- and you'll find that people really listen.",
    "Current book/book you love?": "I really liked \"Olive Kitteridge\" by Elizabeth Strout.",
    "Favorite web site/blog/”guilty pleasure”/fun": "I visit PubMed everyday to see what's news in the field.__Guilty pleasure- Lindt Chocolate Truffles (Dark Chocolate)",
    "Who/what inspires you?": "",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": ""
  },
  {
    "Mentor Name": "nganfhuang",
    "name": "Ngan F Huang",
    "Biography": "Dr. Huang¡¯s laboratory at the Stanford Cardiovascular Institute  aims to understand the chemical and mechanical interactions between extracellular matrix (ECM) proteins and pluripotent stem cells that regulate vascular and myogenic differentiation. The fundamental insights of cell-matrix interactions are applied towards stem cell-based therapies with respect to improving cell survival and regenerative capacity, as well as engineered vascularized tissues for therapeutic implantation. Current projects focus on the role of naturally-derived ECMs to enhance endothelial differentiation of induced pluripotent stem cells on two-dimensional ECM microarrays of varying substrate rigidity. The knowledge gained from understanding cell-ECM interactions are applied towards engineering prevascularized skeletal or cardiac muscle constructs using nanotopographical cues derived from nanofibrillar ECMs.",
    "What do you do every day?": "I do a lot of exciting research to explore new areas. To do that, I have to put ideas into grant proposals and seek out potential funding.  Another aspect of my day is mentoring post-doctoral fellows, medical students, and research assistants. I help groom the next generation of researchers.",
    "Why do you love it?": "I love exploring the unknown and finding new ways to improve health. And with mentorship, I very much like that I am giving back to society, as well, paying forward to thank those who have inspired me in my field.",
    "What were your moments of fear/challenges in your career?": "The fear I recall most is living up to educational standards. In society, we expect students to go to school, to college, and it seems like a very long path. When we are young, we see no option. For me, my perseverance paid off.\nAs far as challenges go, I¡¯ve always been self-motivated. I knew that as long as I worked hard enough, anything is possible.  So, as I was growing up I took on more challenges, such as harder classes, or new extra-curricular activities.",
    "What are some of the innovations in science that you are most excited about?": "I am most excited about tissue engineering that is, growing artificial tissues and organs to replace diseased areas. Creating an organ: that¡¯s as exciting as it gets! We need to understand not only the science but also the engineering of the human body and the function of a normal organ.  This is very complex. Think about it, a heart is a complex organ with an intricate and integral function for life. Creating a heart is not easy, but with the expertise we have already working on tissue engineering, I am confident that we may have engineered organs in 30 years or so.",
    "Where did you grow up?": "Brooklyn, NY",
    "Who was your favorite teacher and why?": "Teachers who love to teach rather than have us memorize are my favorite. That¡¯s why in high school, I really enjoyed my foreign language class teachers, in particular, Mr. Badue, my Spanish literature teacher. These classes were conversational and through gaining experience in speaking a language, we had fun at the same time.\nAlso, what had really gotten me into the field of science was a summer internship offered by the NY Academy of Sciences where I was matched to a lab in the Department of Pathology at Maimonides Medical Center in Brooklyn. There, Dr. Sunny Luke took me under his wing and motivated me to pursue science. This was my defining experience as I spent three summers with this program, and was actually able to publish findings from the work I did with the program on studying genetic abnormalities in patients with ovarian cancer. It is uncommon for a high school student to publish a research paper, so I was really fortunate to have this opportunity.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "When I was going up, I really enjoyed music. I played piano and many other instruments. Unfortunately, my family¡¯s financial situation did not allow me to pursue music lessons. So, I took an opportunity to tutor a junior high school student. This helped me earn enough money to get me those music lessons!",
    "What is your unique talent? (can be something quirky)": "I am ambidextrous, meaning I can write with both my right hand and my left hand. When I was in school, I had a habit of taking notes with one hand, while highlighting with the other!",
    "Personal style/fashion tip? What’s in your purse?": "Actually, I do not wear make-up so much. I prefer a natural look, finding a happy medium! \nAnd I don¡¯t carry a purse because I don¡¯t find it large enough to hold everything I need: my laptop, wallet, etc.  So instead I carry a book bag.",
    "Current book/book you love?": "I read mostly scientific books. But the last non-science book that I read was Lean In by Sheryl Sandberg. I feel this book is very useful for women. I am the only female faculty in my department, so I found some great motivating tips in the book, like jumping in and not being shy.",
    "Favorite web site/blog/”guilty pleasure”/fun": "I like Facebook and reading news, such as CNN.  Occasionally, I like to pamper myself with a relaxing massage.",
    "Who/what inspires you?": "A not for profit organization that I started with my mentor, Dr. Sunny Luke, called the International Institute for Scientific and Academic Collaboration, Inc. (IISAC).  Our aim is to instill the spirit of success and internationalism in young minds through experiential learning, study abroad, mentoring and career seminars. We provide opportunities for students to study abroad in order to create awareness in tropical biodiversity, environmental health, climate change and sustainable development through nature education, field activities and research.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "What¡¯s next? I like what I do, but perhaps if I were not in research, I would look more to the non-profit sector, perhaps something in academic administration and advocate for changes in educational policy. I¡¯m still learning about that."
  },
  {
    "Mentor Name": "yolandabecker",
    "name": "Yolanda Becker",
    "Biography": "Yolanda Becker, MD, is an expert surgeon. She specializes in kidney and pancreas transplantation, dialysis access surgery, and living-donor procedures. Also a respected physician scientist, Dr. Becker is widely known for her clinical research on reducing transplant rejection rates and her basic research in immunology. She has authored more than 100 scientific articles and abstracts in publications, such as the American Journal of Transplantation, Transplantation, and Nephrology Dialysis Transplantation.\nDr. Becker is a featured speaker at medical conferences across the globe, and a recognized leader in the field of transplantation. She serves on the boards of directors for the American Society of Transplantation and the United Network for Organ Sharing.",
    "What do you do every day?": "I am a transplant surgeon.  What is most remarkable about my life is that there is no typical day.  I teach at a medical school, so some days I teach, some days I operate, some days I am in an administrative role as the surgery head of the kidney and pancreas transplant program.  I have two kids, so I am a mom, and I'm also a wife.  Every day is gift and some days are fabulous, a few can be like getting a lump of coal, but the differences make it all so much fun and coal is a good fuel source!",
    "Why do you love it?": "Being a transplant surgeon, I get to help people have a new life.  With one operation, I get to change their lives.  Helping people find meaning through organ donation is also very rewarding- we can offer comfort so that even in death your loved one can still help someone else!  It's a big job, there's a lot to it, and you do have to make choices.  Even if I could make different choices, I would still make the same choices- because it is always worth it.  Nothing worthwhile is ever easy.  It's rare and wonderful to be able to offer respite from misery to people, and I love that.",
    "What were your moments of fear/challenges in your career?": "One of the things I struggle with all the time is balance.  Where do I want to be in 25 years?  I'm very dedicated to my family and kids, and I constantly want to make sure that I can be there for my family!  I worry that it might be easier for my kids if I could be at home all the time but I work because I love what I do.  The balance between personal and professional and the expectations I have for myself and the people around me.  I hate to feel like I am letting anyone down.",
    "What are some of the innovations in science that you are most excited about?": "There's always new discoveries and new medications that come on board that help transplants last longer, medications with fewer side effects.  Knowledge is really exploding- and being able to share that knowledge globally is amazing.",
    "Where did you grow up?": "I grew up in New Orleans, my parents still live there!  I went to Tulane for college and I was on the Homecoming Court!",
    "Who was your favorite teacher and why?": "",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "I play the piano, and I used to ride horses!",
    "Personal style/fashion tip? What’s in your purse?": "Never be afraid to buy a good pair of shoes!  Shoes are your friend!  You never have too many pairs of black shoes.  You have to dress the part, look good and feel good!  Something that makes you feel amazing and smile!   I paint my toenails, and I do nail art on my big toe, because that makes me feel good!  There's nothing wrong with enjoying being a girl.",
    "Current book/book you love?": "I read about a book a week- recently I've read The Nerd Girls with my daughter and The Name of this Book is Secret with my son, and an Amy Tan novel.  The book on my nightstand is The Valley of the Amazement.  _I love Gone with the Wind!",
    "Favorite web site/blog/”guilty pleasure”/fun": "People Magazine!  I read it every Friday.",
    "Who/what inspires you?": "Adversity is a constant, but misery is a choice.\" _John Tarpley, my mentor.  _My mom who is an engineer- and she was one of the only moms growing up who worked.  I was always so proud of her and she would tell me- nothing good comes easy, keep going!  There were really no barriers in the world, except the ones I put out.  And she really taught me that- and gave me a level of confidence that she was always there behind me.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": ""
  },
  {
    "Mentor Name": "reshmasaujani",
    "name": "Reshma Saujani",
    "Biography": "Reshma Saujani is the founder and CEO of Girls Who Code and the former Deputy Public Advocate of New York City. As Executive Director of the Fund for Public Advocacy, Reshma brought together public and private sectors to encourage entrepreneurship and civic engagement across NYC. Today, she has galvanized industry leaders to close the gender gap in STEM education and empower girls to pursue careers in technology and engineering. In 2010, Reshma became the first South Asian woman to run for Congress, promoting smarter policies to spur innovation and job creation. Advocating for a new model of female leadership focused on risk-taking, competition and mentorship, Reshma is also the author of a new book entitled, Women Who Don't Wait in Line, released in October 2013 by Amazon Publishing.",
    "What do you do every day?": "I am the CEO and Founder of Girls Who Code, a national nonprofit organization working to educate, inspire and equip high school girls with skills and resources to pursue opportunities in computing fields.",
    "Why do you love it?": "I love what I do!  Every day I get to work with inspiring young women who are developing skills and experiences that will help change the world.",
    "What were your moments of fear/challenges in your career?": "In 2010, I ran for Congress which was a very different experience for me.  I had never run a political operation before, I had never been on TV beforeÿI did not have a playbook on how to switch from one career to another.   However, this was the best thing that I could have ever done and I learned so much through this process.  I am not afraid to do anything anymore.",
    "What are some of the innovations in science that you are most excited about?": "There are so many innovations in science that I¡¯m excited about.  For me, innovation has to be connected to a problem you are trying to solve.  I really am excited about advances that connect computer science to the life sciences.  For example, there is an innovation underway called the Immunity Project which is comprised of a team of scientists who are coming together to develop a vaccine for HIV.  These are the types of innovations that inspire me",
    "Where did you grow up?": "I grew up in a suburb of Chicago, IL.",
    "Who was your favorite teacher and why?": "I have a couple of favorite teachers.  When I was in the ninth and tenth grade, my parents worked a lot, and I was having a hard time, even getting detentions at school. A couple of teachers saw that all I needed was to be challenged more. They really rallied around me and their support helped turn my life around",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "I have been learning how to listen more and to not necessarily exercise my opinionÿespecially when working with my girls at Girls Who Code. I sometimes want to tell them how to do things but I realize that I need to allow them to learn on their own.",
    "What is your unique talent? (can be something quirky)": "I¡¯m a hustler.  I did not come from great means and have had to learn how to be resilient.  I¡¯ve learned that it¡¯s important to get out of our comfort zones and to have bold asks.   Women should not be afraid to take risks or to fail.  I believe it is better to fail unconventionally than to succeed conventionally.",
    "Personal style/fashion tip? What’s in your purse?": "Dress like you and be you.  I like to wear bright colors and bring in my own style.  It is important in this day and age of Facebook that we are mindful of how we show up there and other social media sites.",
    "Current book/book you love?": "Right now I¡¯m reading Fierce Conversations by Susan Scott.  It¡¯s about mastering communications with your teams as well as in personal situations.",
    "Favorite web site/blog/”guilty pleasure”/fun": "I love hanging out with my dog, Stanley.",
    "Who/what inspires you?": "Hilary Clinton inspires me.  She is a true sister.  She actively supports and sponsors other women.  She also is real.  She¡¯s had a hard time and is a true role model.  Despite some of her hardships, she pushes through and is resilient. She is a true inspiration for all of us who are trying to disrupt conventional leadership.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "Honestly, I am very fulfilled in my current work with Girls Who Code and my work in women¡¯s leadership. I get to work with young women who are fighting every day to gain skills so they can make a better life for themselves. For the first time in my life, everything I am doing is aligned.  I love getting out of the bed in the morning!"
  },
  {
    "Mentor Name": "annlindsay",
    "name": "Ann Lindsay",
    "Biography": "Ann Lindsay MD is Co-Director of Stanford Coordinated Care (SCC). SCC is capitated for primary care of Stanford employees and adult dependents with complex chronic health conditions. Care is provided through a partnership between patients and families and their multidisciplinary care team including physical therapy, behavioral health, nutrition therapy and clinical pharmacy and primary care. Emphasis is placed on the patient¡¯s own goals, care coordination with specialists, and on helping patients gain the skills to be healthy with whatever conditions they faced with. SCC has developed a dashboard that pulls from EPIC EHR to risk assess patients and identify care gaps and a Team Training Center to share the model of care.",
    "What do you do every day?": "I'm co-director for Stanford Coordinated Care, a clinic designed to help people with chronic illnesses lead healthy lives. Half of my day is spent seeing patients and working with my clinical team.  The other half is administrative and teaching time: working with medical students and residents, spreading the model, or getting data together to analyze the effectiveness of what we do and improve our team and care processes.  It's nice to have a mixture of teaching, research and patient care!",
    "Why do you love it?": "I love interacting with patients and getting to know them personally and figuring out what makes them tick!  I love being part of such an effective team- patients get really good care and we have everyone from a pharmacist, dietician, PT and social worker working together.  I have only been at Stanford two years- My husband and I were recruited to build and test out this model of a clinic for a high cost high risk population.",
    "What were your moments of fear/challenges in your career?": "For 28 years I was a family practitioner in a small town in Northern California- running a business and giving good care is a challenge.  For the last 18 years I was also the county health officer and that's challenging because of the responsibility of the population's health and then the politics involved.  Leaving all that and joining Stanford was a huge challenge.  _My husband and I have two children and now we have a beautiful granddaughter- we were fortunate to split one job for ten years so there was always someone at home.  It meant that we both have the opportunity to grow professionally but also both have time for family life.",
    "What are some of the innovations in science that you are most excited about?": "There are tremendous technological innovations- I find the challenge is getting people who have chronic illnesses motivated to do something to better their health. There are innovative models of care working with patients from many different social and cultural backgrounds. I love being part of that and feel what we are doing is reproducible and can make an impact!",
    "Where did you grow up?": "I grew up in a small town in Massachusetts.",
    "Who was your favorite teacher and why?": "I was influenced most by a friend's mother- who was a physician!  She was a wonderful mentor for me- I didn't know what I wanted to do, but she would always urge me to talk to female physicians and learn from their experiences!   It really changed my life and perspective.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "Bringing people together in a community around a problem to solve it!  __I believe in \"never giving up!",
    "Personal style/fashion tip? What’s in your purse?": "Be natural!  You can't be too flamboyant- you have a lot of freedom but you do get judged by what you wear!  Have confidence in your body!",
    "Current book/book you love?": "I love the book \"Cutting for Stone\" by Abraham Verghese.  It starts in Ethiopia, with identical twins whose parents are physicians and just follows their incredible stories!  It's an amazing look at being a physician and what that entails and the whole training process and how you learn how to take care of people and put them in a position of priority.  It looks at FMG (foreign medical graduates) in a better light and highlights the challenges they overcome.  It's extremely inspirational!",
    "Favorite web site/blog/”guilty pleasure”/fun": "",
    "Who/what inspires you?": "",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "I'm looking forward to working on research to show that our model here is working- our focus on patient goals can be the answer to adverse health outcomes and medical care in this country."
  },
  {
    "Mentor Name": "lidiafonseca",
    "name": "Lidia Fonseca",
    "Biography": "",
    "What do you do every day?": "I create data and technology solutions for physicians and patients.",
    "Why do you love it?": "Data and technology help us serve physicians and hospitals to improve patient health.",
    "What were your moments of fear/challenges in your career?": "Ensuring that we process lab specimens on time.  Doctors use our lab results to make life and death decisions about their patients so it is essential our results are timely and accurate.",
    "What are some of the innovations in science that you are most excited about?": "The advances in genetics and next generation sequencing are fascinating.  Tracing the cause of a disease to genetics can be the breakthrough to manage serious diseases and even prevent them!",
    "Where did you grow up?": "I grew up in Mexico.",
    "Who was your favorite teacher and why?": "Mr. Jensen in middle school--he saw potential in me that I did not know myself. he encouraged me to read the classics and apply to a magnet high school. That was a pivotal point in my life.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "I am very goal oriented and execution driven.  In my first leadership role I was in charge of many older individuals.  When I became head of the group, I could see they were skeptical.  Even though I was in charge, I asked for their opinion as to what I could do better.  I think to be a good leader you must be prepared to also follow.  That softened my team up and we accomplished great things together after a shaky start.",
    "What is your unique talent? (can be something quirky)": "I am a change agent, I take on projects that others think are \"mission impossible.\"  I see the opportunity and envision how it will be when we transform.",
    "Personal style/fashion tip? What’s in your purse?": "A great moisturizer, mints and a good lip gloss.",
    "Current book/book you love?": "Anything by Jim Collins - he illustrates why some companies thrive by re-inventing themselves on an ongoing basis",
    "Favorite web site/blog/”guilty pleasure”/fun": "I watch Scandal and Dance Moms... Shhh, don't tell anyone!",
    "Who/what inspires you?": "My 9 year old twin boys.  They constantly remind me that we should enjoy the simple things in life and to take in the wonders around us.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "My two life goals are to join the board of a public company and to teach at a business school.  On May 1st I was elected to the board of a public company.  Next is to land the opportunity to teach at a business school.  That is how I see my retirement--serving on a couple boards and teaching."
  },
  {
    "Mentor Name": "andreamcgonigle",
    "name": "Andrea Mcgonigle",
    "Biography": "She currently serves on the Clinical Advisory Committee for the Pacific Business Group on Health CMMI supported project, Intensive Outpatient Care Program, which seeks to enroll 27,000 patients in three states by 2015.  She is a fellow in the California Health Care Foundation Leadership Program and joined the IHI (Institute for Health Improvement) faculty in October, 2013.",
    "What do you do every day?": "I look at the issues the Health & Life Science industry is facing and I look at the roadmap of Microsoft technologies and ask myself what we can do together to  make an impact on the Health & Life Science industry.",
    "Why do you love it?": "I really believe in the company I work for and their mission. I love knowing the things that I do are making an impact to improve health & life sciences. I also love that this role allows me to excel at a national level but gives me the flexibility to be a good parent at the same time.",
    "What were your moments of fear/challenges in your career?": "Pharma layoffs have become a common occurrence in the past few years.  11 years at a company and to come in one day and find out it's your last day is a tough situation and it was one that I encountered. It's what you do in that moment that makes your stronger or leaves you behind to wither. It gave me time to focus on me and determine what I want to do with my life. Instead of jumping at the first opportunity, I made a short list of companies I would work for. I then put every effort into landing a role where I could share my passion, feel like I was making an impact and still have a work-life balance. What seemed at the time to be dark moment or challenge in my career, became a pivot point that helped me skyrocket to the next level. I have never looked back and realized it was one of the best things that ever happened to me.",
    "What are some of the innovations in science that you are most excited about?": "I am most excited about the world of personalized medicine and diagnostic testing. When I think of the implications that technologies such as analytics and the cloud can have in this space, it brings us light years ahead in how we could treat patients, cure illness and lower costs in our healthcare system.",
    "Where did you grow up?": "I was born in Belfast, North Ireland but grew up in Upper Darby, PA",
    "Who was your favorite teacher and why?": "My favorite teacher was Sister Dr. Shawn Margaret Fagan. She was young and energetic. She knew how to make learning fun.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "My approach is always stick to the facts and remove emotions. There are many situations where I read an email or a decision is made and I want to blast a comment back or yell out, \"you have got to be kidding me!\" but I don't. I try to let those emails sit, wait to the next day and then take a very factual approach to my response. That helps to make a very high quality discussion where things are driven to results rather than on emotion.",
    "What is your unique talent? (can be something quirky)": "Calligraphy. Not many people do it, I taught myself but it is a dying art.",
    "Personal style/fashion tip? What’s in your purse?": "I love to pick a color each season and revolve my outfits around a specific bag. Coral nails are my trademark nail color.",
    "Current book/book you love?": "Lean In . I love it and created a book club with a group of women on it.",
    "Favorite web site/blog/”guilty pleasure”/fun": "Guilty pleasure: General Hospital  After a stressful day at work, I love to decompress after the kids go to bed and watch General.",
    "Who/what inspires you?": "My mom and dad. They are immigrants from Northern Ireland. They left the family and life they knew to give their kids a better life. They have defined the word sacrifice.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "I am very involved today in education at the grade school and college level. I love seeing the kids react to technology and I get inspired thinking I can make a difference in the lives of girls and boys and open their minds to a career in science or technology. I see myself doing something more formally in this space when I retire."
  },
  {
    "Mentor Name": "laurepark",
    "name": "Laure Park",
    "Biography": "",
    "What do you do every day?": "I am responsible for leading our  Prescription Drug Monitoring & Clinical Toxicology business, driving growth, expanding our market share and enhancing our position as an industry thought leader.",
    "Why do you love it?": "I love interacting with customers and finding solutions to meet their needs.  Every day is different.",
    "What were your moments of fear/challenges in your career?": "The biggest challenge in my career were the points when I accepted stretch roles that moved me not just into bigger roles, but also had me leading areas that were beyond my prior experiences.",
    "What are some of the innovations in science that you are most excited about?": "The advances in diagnostics are very exciting.  We are now able to learn so much about us, such as our individual genetic make-up. This truly makes it possible to customize diagnostic protocols in the care of an individual.",
    "Where did you grow up?": "I grew up on a farm in North Dakota.",
    "Who was your favorite teacher and why?": "I loved my English teacher, who was also my speech & drama coach.  I actually just tried to re-connect with her.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "I have a great memory of trivia.",
    "Personal style/fashion tip? What’s in your purse?": "I am a classic dresser who loves bold accessories.  In my purse today is a smart phone, wallet, lipstick, pen, business cards and headphones.",
    "Current book/book you love?": "The End of Life Book Club.  It is a beautiful story on gracefully dealing with aging and illness, with a list of great reading to boot.",
    "Favorite web site/blog/”guilty pleasure”/fun": "People, of course.",
    "Who/what inspires you?": "I am inspired by young girls around the world that are putting themselves in danger to get an education.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "I don't know what is next for me.  My philosophy is \"yes, and...\" when presented with a challenge.  My litmus test is always, \"is it worth the time away from my family?"
  },
  {
    "Mentor Name": "sarahwamala",
    "name": "Sarah Wamala",
    "Biography": "Prior to moving to Stanford in 2011, Dr Lindsay shared a family practice with her husband, Dr Alan Glaseroff, in rural Northern California for 28 years. During this time she served as County Health Officer for 18 years and was active in the leadership of the California Conference of Local Health Officers in Sacramento.  In 2006 she received the Plessner Award from the California Medical Association as the physician who best exemplified the practice and ethics of a rural practitioner",
    "What do you do every day?": "Meetings most of the day, going through reports on important current issues, state of public health in Sweden and giving feedback, strategic meetings to determine policies that will shape the population health in Sweden and globally",
    "Why do you love it?": "The things we do may affect many people's health- not just one person's health.  It has a larger impact on all human beings.",
    "What were your moments of fear/challenges in your career?": "Finding a balance between economic issues and public health- for example, tobacco products that are harmful to health, but do generate revenue.",
    "What are some of the innovations in science that you are most excited about?": "Systematic ways for politicians to understand the scientific basis of the policies we suggest. To push for hard science as the underlying reason to choose certain policies.",
    "Where did you grow up?": "I grew up in a small village in Africa, in Uganda- I walked to school every day, grew up with my mother and grandmother, carrying water and living on a farm with no television. I was the first person to go to university from the village.",
    "Who was your favorite teacher and why?": "My physics teacher, Peter, who taught me to love the sciences during primary school.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "One time, as a manager, we had a change of political priorities and my team was not happy with what was going on.  I grabbed a mic and started to sing- to cheer people up, and bring the team together.",
    "What is your unique talent? (can be something quirky)": "I love singing and dancing.",
    "Personal style/fashion tip? What’s in your purse?": "",
    "Current book/book you love?": "Thinking, Fast and Slow by Daniel Kahneman",
    "Favorite web site/blog/”guilty pleasure”/fun": "",
    "Who/what inspires you?": "",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "I want to be able to change people's lives on a global level."
  },
  {
    "Mentor Name": "jeaninemartin",
    "name": "Jeanine Martin",
    "Biography": "Jeanine Martin is no stranger to the healthcare and technology industry. A co-developer of innovative healthcare solutions on the Microsoft platform, she is responsible for many current technological breakthroughs such as the Xbox Kinect, Windows Phone 7, and surface computing. She is also an exclusive member of Microsoft¡¯s Global Health Strategy Committee, Microsoft¡¯s Global Health Executive Briefing Speaker¡¯s Bureau, and the Microsoft-HIMSS Healthcare User Group liaison. She formed Microsoft¡¯s 1st National Cross-Disciplinary Clinical Informatics Council and their 1st Health Provider Advisory Council and she was the dedicated Global ¡°CRM in healthcare¡± SME on the team. Martin is a Nurse Advocate who has spent the last 20 years in the Health IT industry, recently accepted into the ONC-funded Johns Hopkins School of Medicine Clinical Informatics program.",
    "What do you do every day?": "Director of National Healthcare at Avanade, Inc (Microsoft/Accenture Joint Venture) who is responsible for driving innovative Healthcare technology solutions/services built on the Microsoft platform into the US Health & Life Sciences market space.",
    "Why do you love it?": "I have a passion for the vertical healthcare technology industry that is capable of impacting global change in the areas of Health, Wellness and Fitness.",
    "What were your moments of fear/challenges in your career?": "My biggest challenge was to break \"the glass ceiling\" as a Women in the Healthcare Technology Industry by leading with compassion, competence and confidence.",
    "What are some of the innovations in science that you are most excited about?": "Working with a client on a new Healthcare business model that would leverage innovative Virtual Health technology to migrate away from the chronic condition management market in a hospital setting and towards health & wellness at home.",
    "Where did you grow up?": "Born in Boston, MA; Raised in Marin County (CA); Living in Nashville, TN now",
    "Who was your favorite teacher and why?": "Favorite Teacher was my Sports Coach who gave me the confidence to play Olympic-level tennis",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "I hosted the 1st National Health IT Summit where we had to connect similar organizations in the industry who traditionally did not cross-collaborate.  We bridged that gap by driving a common goal albeit controversial, namely; semantic interoperability.",
    "What is your unique talent? (can be something quirky)": "Connecting People",
    "Personal style/fashion tip? What’s in your purse?": "I love a good pair of high heeled shoes.  My best fashion advice is to wear what makes you feel comfortable.  I typically keep my wallet, make-up, cell phone, etc. in my purse.",
    "Current book/book you love?": "Never Eat Lunch Alone by Keith Ferrazzi",
    "Favorite web site/blog/”guilty pleasure”/fun": "HISTalk-online HIT social media site",
    "Who/what inspires you?": "My children who inspire me to improve the HIT system",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "Would love to help lead a company in the Health, Wellness & Fitness Industry"
  },
  {
    "Mentor Name": "akhilasatish",
    "name": "Akhila Satish",
    "Biography": "Akhila Satish is a scientist and entrepreneur and is currently the CEO and founder of CyberDoctor, a healthcare communications company.  CyberDoctor was an early pioneer in the use of technology solutions to improve the patient physician interaction and patient adherence to treatments.  The company has met with tremendous success, with its products sparking discussion and thought globally. Cyber Doctor's academic approach to healthcare technology- focusing on the final, measurable clinical outcome of the patient experience- is strongly influenced by Akhila¡¯s experiences within academia. \n CyberDoctor¡¯s latest app, PatientPartner, is the first application to be proven effective in significantly improving adherence and biological markers in diabetic patients. This groundbreaking app was recommended by a number of diabetes organizations and media outlets including A Sweet Life and DiabetesMine among others.  Akhila has received numerous accolades and honors for her work on CyberDoctor; notably, she was honored as a Rising Star at Health 2.0 in 2013, a semifinalist in the Healthcare Innovation World Cup, a Global Leader in Innovation and Entrepreneurship by the Center for Healthcare Innovation.  \nAkhila is passionate about advocacy work and her recent efforts include serving\non the board of the Women in Healthcare and Life Sciences, a global effort to promote girls in STEM.  This summer, she launches The Science Runway, a nonprofit website designed to inspire young girls to join the sciences.  T.  \nAkhila is a frequent speaker at a variety of healthcare conferences and universities.  She speaks on issues of scientific literacy, the transition from research to entrepreneurship and the importance of clinically proven technologies in the healthcare technology marketplace.  \nShe previously worked in life sciences research at the University of Michigan and the National Institutes of Health.  Her published work includes papers in Nature and Human Genomics.  Several of her articles on scientific literacy have appeared in Forbes.  Currently, she blogs at the Huffington Post as part of a project to help translate scientific journal articles in a way that is accessible for everyone, not just those who are scientifically trained.   \nAkhila received her Bachelor of Science in neuroscience with honors from the University of Michigan. She holds a graduate degree in biotechnology from the University of Pennsylvania and graduated from the Stanford Graduate School of Business Summer Institute for Entrepreneurship (IGNITE).",
    "What do you do every day?": "I¡¯m the CEO and Founder of CyberDoctor, a healthcare communications company.  We build products that help patients engage with the healthcare system in a more meaningful way.  So I spend a lot of my day looking at data around our products, figuring out new things we can do, new companies we can partner with and how we get our products to patients.",
    "Why do you love it?": "I love that what I do makes an impact.  I love being able to measure that impact and make choices based on it.  My job allows me to be a scientist, be an innovator and use technology in a new way.",
    "What were your moments of fear/challenges in your career?": "My biggest challenge was figuring out what my ideal job would be and then crafting a path toward it.  I¡¯ve flirted with many career paths- from law to architecture!  I have seriously considered medicine and I spent years working in research.  I knew what I wanted was a high impact job that allowed me intellectual flexibility and kept me grounded scientifically.  As I worked my way through different options, I kept focused on that goal and I think it¡¯s the reason why I am where I am today.  You can¡¯t be afraid to shift directions- life¡¯s too short and you work too many hours to work in a job you aren¡¯t happy with.   Follow your heart.",
    "What are some of the innovations in science that you are most excited about?": "I am energized by so many different aspects of science!  I find tissue engineering fascinating- I think some of the new work around immortality  and neuron regrowth is incredible.  Most of all, I¡¯m always excited about a well designed, well thought through experiment in science!",
    "Where did you grow up?": "I grew up in Syracuse, NY- a snowy university town with the best basketball team in the country!",
    "Who was your favorite teacher and why?": "I was lucky to have some incredible teachers along the way.  My US history teacher from high school really taught me to think analytically, and by teaching a really difficult, work intensive course, prepared me very well for college and graduate school!  My quiz bowl coach taught me a lot about leadership and was so supportive of my growth as a team captain and team player.  I had incredible math and english teachers as well.  In undergrad and graduate school I found strong science mentors who helped me grow as a scientist.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "",
    "Personal style/fashion tip? What’s in your purse?": "Be bold, brilliant and beautiful.  Never be afraid to look your very best because you doubt that you will be taken seriously.  Prove to the world that you can be everything you want to be, and let your fashion express that in a tasteful and classy manner.",
    "Current book/book you love?": "Voices of a People¡¯s History- Howard Zinn; The Origin of Species- Charles Darwin; The Iliad- Homer; The Side of Paradise- F. Scott Fitzgerald; anything by LM Montgomery",
    "Favorite web site/blog/”guilty pleasure”/fun": "I read everything I can possibly find to read online!  I look through the NYTimes, the Wall Street Journal, the Smithsonian Magazine online, Nature, Slate, Forbes and Huffington Post (where I blog currently).  I try to read things I really disagree with as much as things I agree with- it¡¯s so easy to live in a silo of agreeable knowledge these days even though we have so much more access!",
    "Who/what inspires you?": "I'm inspired by people who exhibit true grace under pressure, who embody the Renaissance spirit of gaining knowledge for the sake of knowledge and who truly want to make the world a better place.  My family, my friends, fellow entrepreneurs- I feel so lucky to have them in my life to support and inspire me on a personal level!",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": ""
  },
  {
    "Mentor Name": "lydiagreen",
    "name": "Lydia Green",
    "Biography": "A pharmacist, clinical strategist, and medical writer with extensive experience in direct-to-physician promotion, Lydia¡¯s core strengths are understanding how to utilize clinical evidence, message framing and emotional appeal tocommunicate medical evidence- accelerating adoption of best practices, promoting behavior change and leading to the rational utilization of drugs, devices and diagnostics.\nFor the past 14 years, she has held various communication positions at Epocrates, including Director of Corporate Communications, Manager Editor of Medical Education and Creative Director, Marketing. In her current consulting position as Acting Director of Sponsored Content Strategy, she helps healthcare companies design mobile communication programs targeted to healthcare professionals. Prior to Epocrates, Ms. Green worked in a senior-level communication position at a large global medical advertising agency in New York. A versatile writer, her past clients include the Prescription Project, Public Library of Science, Montana State Pharmaceutical Association, and the American Medical Association.\nLydia has a B.S in Pharmacy from Massachusetts College of Pharmacy and is a licensed pharmacist in Montana.",
    "What do you do every day?": "I research pharmaceutical drugs, medical devices and disease and create medical content for promotional purposes.",
    "Why do you love it?": "I am constantly learning.  I love the challenge of learning about something totally new and explaining it to others that is clear and comprehensible. There is constant change and variety of the projects.",
    "What were your moments of fear/challenges in your career?": "I have worked as a freelance medical mareketing writer as well as a fulltime medical marketing writer.  The greatest challenge was the first seven years of my career when I didn't have confidence that I could always produce high quality content on demand.",
    "What are some of the innovations in science that you are most excited about?": "I am most excited about personalized medicine for cancer care.  It is exciting how genetics testing can provide information on which patients will respond to a particular type of therapy.",
    "Where did you grow up?": "South Orange, NJ",
    "Who was your favorite teacher and why?": "",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "",
    "Personal style/fashion tip? What’s in your purse?": "",
    "Current book/book you love?": "The Autobiography of Henry Ford and First Person Accounts of Women in American History",
    "Favorite web site/blog/”guilty pleasure”/fun": "Cafe Pharma",
    "Who/what inspires you?": "Entrepreneurs that change the world.  Dorothy Day and Gladys Aylward",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "I am starting Rx Balance, a non-profit in healthcare communications, by applying pharmaceutical strategies to public health."
  },
  {
    "Mentor Name": "melvacovington",
    "name": "Melva Covington",
    "Biography": "Melva is currently a leader within the North American R&D Hub at Sanofi. Her leadership skills, expertise and impact has spanned throughout the drug development lifecycle process for over 15 years. She has a broad background in health services research with the application of critical thinking, business management and scientific expertise to collaborative address complex issues within the healthcare community.",
    "What do you do every day?": "Every day I think about new and better ways of doing things. I am trained in the disciplines of Public Health and Early Intervention.  So by training, I am focused on population health among in various diverse groups and the diversity of ideas and approaches to address solutions.  Specifically, I seek to understand and provide solutions on ways to help and support patients and communities, i.e., access to health care for individuals, working with communities of individuals, families, regions, payors, society and professional colleagues relative to the appropriate delivery of health care services.  Each day, I have different things to do in my R&D role improving recruitment and retention in clinical research.  I focus on prioritizing what needs to be done and how to do it efficiently with the resources available to me. However, my thoughts are always about how I can use my skills and talents, in partnership my very bright colleagues, to come up with outcomes that will improve health and wellness of people/families.",
    "Why do you love it?": "I love what I do because I approach each situation or tasks with the mindset of how it will be successful and make an impact.  Now that outcome is not always so evident because usually the challenges and barriers are great.  However, that doesn¡¯t impact my mindset of excellence, even if it does not look so good. I approach every circumstance as a way to make things better and exceed expectations.  My ¡°job¡± is to see the possibilities, use what we have (or can create) to build and execute to produce on something innovative.",
    "What were your moments of fear/challenges in your career?": "One of my greatest challenges was in preparing the final versioncomponents of my Ph.D. dissertation. I had to integrate the latest changes in the document based on input from my advisors, finalize it in 24 hours and turn it into the Registrar in order to graduate. These were the days, in which we used floppy disks to save things because the computer hard drive storage was not large enough.  Well, I finished the changes and went to save. But before I could do so, the entire computer system crashed, damaged the disk and I lost all of the written changes in the process.   \n\nI was heart-broken, walked out of the computer lab, sat on the floor, started crying and just prayed for comfort/help/direction _ anything!  I saw my life flash in front of me because it was due at 5pm and it was 4:45pm.  At that very moment, my dissertation Cchairperson happened to walk out of the class room to get something from his office and saw me there, looking miserable.  I explained what had just happened and he arranged for me to have another 24 hours with the registrar to make changes.  I went back to the latest version that I had on a separate disk and got the job done.  \n\nLife lesson:  Never panic _ everything is manageable!.  That experience guides my reaction, even now, in crisis management and building solutions.",
    "What are some of the innovations in science that you are most excited about?": "I am most excited about the breakthrough in Genomics and the potential of innovation in targeted (or tailored or personalized) medicine.  The breakthroughs in understanding the DNA structure of all living things (and particularly in the human race) enables us to better understand the cycle or pattern of diseases and develop therapies that target them , while limiting side effect profiles.   This is coupled with the explosion in technology and the use of automated systems to replicate and analyze information much faster than ever imagined is simply amazing. This innovation and its precise the application across populations of it in increasingly precise ways are is revolutionary.",
    "Where did you grow up?": "I grew up in Northeast Washington DC.",
    "Who was your favorite teacher and why?": "My favorite school teacher is my mother, who was my first teacher of life, information and culture.  She established in me the key concept to understanding that ¡°nothing is impossible _ so go ahead and soar!¡± She was not only a phenomenal role-model but also taught business to junior and senior high school students in the DC school system for 46 years. \n\nAside from my Mom, Mr. Greene was my favorite teacher who taught me in the 7th grade. She was a little woman who helped me to make a good transition into junior high school and was a gentle _ yet firm disciplinarian.  I was able to go to Europe under her watch and she nurtured experiences/exposures outside of America.  My exposure to the world and global possibilities was birthed from her mentorship. That is why mentorship is so important to me now.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "I moved from NJ to Indianapolis in 2004 to take a new job.  I had no family or friends there, but wanted to use this as an opportunity to adapt my social and professional style to successfully live in the Midwest _ very unlike the Northeast.  Nearly everything was different _ even the rate of speech. People keep asking me to slow down and repeat myself. Nevertheless, this was an opportunity for me to understand amy new environment, listen to people carefully and drop my perceptions of ¡°what was normal¡± so as to be more open to change. This required me to empathically look at things from the eyes of others but also be comfortable in bringing ¡°my authentic¡± self to the table _ and that was alright.",
    "What is your unique talent? (can be something quirky)": "My talent is in synthesizing complexity.  I am not sure how unique it is. However, I have a gift of being able to digest complex concepts (or things that don¡¯t seem to go together well) and develop patterns or develop a strategy from diverse pieces.  These connections just seem to flow together in my mind. I then use the synthesized concepts to dialogue and motivate engage with others.  This stimulates great conversations and long lasting real collaborations.",
    "Personal style/fashion tip? What’s in your purse?": "Personal style _ custom, monogrammed French cuff shirts with cufflinks (usually color matched).  For me, it is a silent power statement when a woman enters in a room; it says (for me) she means business, so don¡¯t play. Also, a nice pair of heels goes well with that! In my purse is my cell phone, money clip and hand sanitizer.",
    "Current book/book you love?": "I generally read multiple books at one time _ I get bored easily so this is necessary to keep my brain stimulated.  Right now, I am reading four books:  a.\tCorner Office Rules, Keith Wyche\nb.\tA Pale Horse, epic novel by Wendy Alec\nc.\tJesus>Religion, Jefferson Bethike\nd.\tDavid and Goliath, Malcolm Gladwell",
    "Favorite web site/blog/”guilty pleasure”/fun": "Favorite website is MotorTrend, Linked.in, CNN, Spafinders.   I am also a bicycle rider so I explore different trials or vacation where I can bike in nature.",
    "Who/what inspires you?": "What inspires me is the life and stories of Jesus Christ of Nazareth. Understanding His walk and impact as He engaged with on people is a constant source of inspiration and way to model my life.  I am not nearly as perfect, but as He is. ; but Therefore, I try to think about love, compassion and grace the way that He did _ and pattern my life and decisions based on it..",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "What is next for me is to continue to work to bring solutions through innovation to people, communities and my company.  As Sanofi continues to evolve in thise constantly changing healthcare eco-system, I hope that I can play a part in that transformation.  In particular, I would like to contribute to the understanding of how diverse patient populations and communities can benefit from the healthcare solutions that we generate within the pharmaceutical industry. We are currently engaged in building research structures and commercial platforms that enable us to be more patient-centered.  A key part of this is having Participatory Action Research and Patient Engagement opportunities that help us to be better partners in building healthcare solutions. I would also hope to be an inspiration to the next four generations of scientists.  An impactful woman leaves an inheritance to the next few generations."
  },
  {
    "Mentor Name": "tanle",
    "name": "Tangle",
    "Biography": "",
    "What do you do every day?": "What's unusual about my job is that I work with a larger number of women than I am usually used to.   It's very different from the tech world in general, where there are more men than women on executive committees.  It's a very collaborative and nurturing environment- we are all friends and colleagues.  \n\nWe have a very distributed team- people work in different parts of the globe, different time zones and so it's a much more flexible working environment.",
    "Why do you love it?": "One of the greatest things about the work we do is that we want to democratize the space around brain research.  We have the opportunity to transform lives in a significant way- and this mission really resonates with our team.  As a result, the team finds it easier to live a meaningful life!",
    "What were your moments of fear/challenges in your career?": "A lot of us spent much of our life finding what we are passionate about- and I was just like that.  I wanted to find something that would captivate my heart and imagination.  I was always very reflective, and so I really wanted to find my passion.  As a teenager, I did community service to help people find vocational work and education that would help people find a job.  It mattered to me that I was trying to do something positive.  I started my career in law, at a large law firm in Australia.  As I was working there, we started a section of the firm that serviced innovators and entrepreneurs- as I moved over and became more and more interested, I found that the digital revolution and information age was transformative and I wanted to be a part of the action.  And that's when I made the change!  It has to be the unique fusion of inspiration, ideas, and the right mix of people- and when I ran into the area of brain research, I was completely crazy over it.  I felt brain research was really ripe for innovation.  I didn't want to compromise- I wanted to create something new that would tackle a difficult problem.",
    "What are some of the innovations in science that you are most excited about?": "Biotechnology, energy (green, renewable etc.), I'm excited about social impact organizations as well!",
    "Where did you grow up?": "Melbourne, Australia",
    "Who was your favorite teacher and why?": "My primary school teachers- it was a Catholic school, and a very nurturing, value filled environment.  I learned so much about being grateful and needing to give back!  The high school I went to was focused not only on academics but also finding passion in your work.  It really brought out the best in me and helped me find my inner strength and confidence.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "I'm finally developing a green thumb!  I thought I was terrible with plants- but in the past two years, I've developed a nice little garden!  It's teaching me patience, and I love it.",
    "Personal style/fashion tip? What’s in your purse?": "My purse is full of credit cards- too many!  Fashion wise, I like classic pieces with a pop of color.",
    "Current book/book you love?": "",
    "Favorite web site/blog/”guilty pleasure”/fun": "I really enjoy Pinterest!  I like collating ideas and tidbits on there- from remodeling tips to gardening ideas.",
    "Who/what inspires you?": "My mom- she's an incredibly strong role model for me.  She came to Australia with just my sister and me- she has worked so hard to give my sister and I a great start to life.  She is the most incredible inspiration- raised two kids on her own and earned two degrees and is the first Vietnamese mayor outside of Vietnam!  She is such a positive, optimistic person with such a healthy outlook on life.  She's incredibly disciplined too.  Just seeing her, I realize that she has the most amazing amount of strength and discipline.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": ""
  },
  {
    "Mentor Name": "caoimhekiely",
    "name": "Cao Imhekiely",
    "Biography": "Prior to joining she led Global and US-based teams in Health Outcomes and Pharmacoeconomics across a number of therapeutic areas at Lilly and Roche labs. She has cross disciplinary experience and training in a number of areas, namely maternal and child health, clinical development, health outcomes, public policy and business management. Her goal is to apply knowledge both broadly to understand the patterns of disease and prevention as well as more specifically to address the needs of people.",
    "What do you do every day?": "As Vice President of Marketing I am responsible for providing strategic direction and driving company growth through global marketing, with a focus on demand generation and building the sales pipeline (B2B). \nI create and plan marketing communications and execute marketing campaigns across Product Launch, Telemarketing, Prospecting, Industry Events, User Conferences/Customer Nurturing, Partnerships, Analyst and Press Relations, Web, SEO and Social Media.",
    "Why do you love it?": "My job, as part of a global software company, is always varied and never dull.  Our software solutions enable life sciences companies to meet global regulations for researching and manufacturing drugs and medical devices. I work in an industry that is always changing, always adapting and always trying to improve lives health and cure illness. I meet truly inspirational people who dedicate their entire lives to learning about illness with the purpose of finding a cure for it. Our software enables them to do this in a regulated way, with control and quality paramount through the entire lifecycle of development of drugs and devices.",
    "What were your moments of fear/challenges in your career?": "It was a difficult learning curve in the beginning--getting up to speed on a complex product for a complicated industry. But it was an exciting challenge, and even after 11 years in this company, I'm challenged daily with new learning. I took two extended maternity leaves in the last decade, and both times feared the return to work, getting the work/life balance right, and ramping back up after spending several months with babies and toddlers. I believe women can have it all. The stereotypes still exist, even subconsciously, so it's a constant challenge to stand up for what you believe in.",
    "What are some of the innovations in science that you are most excited about?": "Personalized medicine is awesome. It has its challenges, but I think the move away from 'one drug fits all / bulk manufacture' is the future of medicine and will truly enable us to view and address illness differently. Technology is changing to keep pace, and together with personalized treatment offers huge opportunity.",
    "Where did you grow up?": "Dublin, Ireland.",
    "Who was your favorite teacher and why?": "I didn't like any of my high/secondary school teachers very much but I really liked my university lecturers and professors, many of whom were extremely knowledgeable and inspiring. I've met some of my favorite teachers in my professional life, many of whom are colleagues.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "In general I try to avoid confrontation at all costs (a personal trait or fault!), but sometimes you have to be stronger or more aggressive than you naturally are, particularly in the business world. I regularly have to adapt my approach to be more forthright and aggressive in ¡®sticky¡¯ situations, to make progress or resolve issues with strong, global teams.",
    "What is your unique talent? (can be something quirky)": "I generally like people and want to get to know them and get along with them.  This could be considered a talent in Marketing as it's all about engaging people. I can hold a seriously technical conversation with board level decision makers, but also chat about what matters to people, their kids, plans, travels etc.",
    "Personal style/fashion tip? What’s in your purse?": "I prefer to be over-dressed than under-dressed. I leave trendy/edgy outfits for nights out with my friends or crazy sisters, and aim for elegant in work - Kate Middleton's clothes- simple, knee length dresses with sleeves are my preference, with a pair of pumps, and are perfect for the office. I always have a hairbrush, lipstick, iPad mini and iPhone in my purse.",
    "Current book/book you love?": "I'm reading the 'Divergent' series at the moment, as a recommended follow on to Game of Thrones. I love the classics, particularly Pride & Prejudice, but read just about anything. In case I read too much candyfloss, I always aim to read the Booker Prize list annually.",
    "Favorite web site/blog/”guilty pleasure”/fun": "Any book on my iPAD Kindle app",
    "Who/what inspires you?": "My friends, my family, and my kids.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "My company has just been acquired by a much larger company.  I'm excited to see where this takes me and what new opportunities I'll get!"
  },
  {
    "Mentor Name": "cristalthomas",
    "name": "Cristal Thomas",
    "Biography": "",
    "What do you do every day?": "My job as deputy governor is to help Gov. Pat Quinn manage the State of Illinois.  That can mean many different things over the course of a day- there are many different work projects that I participate in.  My work,  in terms of my responsibilities fall into 3 buckets- 1) the actual policy work requires implementing Governor Quinn¡¯s policy agenda, working with senior staff, working with members of cabinet, and the things the governor cares about- retaining jobs, improving healthcare access and better education; 2).  the second bucket is outreach- speaking to groups and reaching out to the media so people know what we are doing; and 3).  the third bucket is interacting with different legislators and making legislative decisions and to help them understand how their budgetary decisions play out operationally.",
    "Why do you love it?": "I love several things about my job- it's really interesting because when i first started out in scienceÿ.I was passionate about wanting to know how things work and had a thirst for knowledge.  Making the jump into government is actually similar- i like to get to know how things work from a system point of a view- policy wise.  But I¡¯d say what I love most is the opportunity to make a ¡°different¡± difference, improve people¡¯s lives and be in a position to be constantly learning and challenged.  That is  what makes me jump out of  bed in the morning.",
    "What were your moments of fear/challenges in your career?": "in my career, and I think this is very translatable, I deal with important, big and complex issues.  We are dealing with things that impact people's lives directly.  it's very daunting to operate in an environment of imperfect information- it's scary to jump out there and start on a path with the understanding that you have to figure it out as you go.  My science background helps me with this- you are trained to figure out a hypothesis and test it- and if it doesn't work, you adjust and it takes you in a different direction.  The process of making and understanding policy is very similar.  The difference for me in a government context is that you are dealing with a more unforgiving environment- everyone expects you to know, and they don't see a value proposition in the learning process.",
    "What are some of the innovations in science that you are most excited about?": "I work in the area of translation- the impact side of intersection , where science meets policy. I live and see most things!.  The best example is in health care policy.  Advances in  medical technology- such as: what is the best most effective delivery system to get a drug to a person?  The advances in genetics that can lead to personalized medicine....we don't know what that will mean for cost, but the ability to personalize a treatment plan could have huge positive impacts.  I'm also very excited about the field of nanotechnology-  we have here at Northwestern University here in Chicago a hub for this,  and this field has great potential across the board for healthcare disciplines.",
    "Where did you grow up?": "I grew up in a town called Portsmouth, Ohio.  It's a pretty small town on the Ohio River across from Kentucky.",
    "Who was your favorite teacher and why?": "",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "The challenge I had was when I made the switch from working in science to working in policy.  In science you do tend to work in teams and collaborate and it is very clear-cut.  Policy is a bit messier- to say the least-  and that background is so helpful to approach problems in a logical and systematic way.  What I found was a strong backlash against my version of collaboration- you have to compromise to collaborate, which you don't in science.  When I first started working in state government, I felt very frustrated because things weren't working as quickly as I wanted.  I figured out how that needed to change and how to work more in teams and accept and recognize in policy the process of compromise is necessary and can be beneficial.  In general, that's what people are finding in the science world around crowdsourcing.",
    "What is your unique talent? (can be something quirky)": "",
    "Personal style/fashion tip? What’s in your purse?": "My style has evolved so much, but slowly over time.  I started off as a tomboy- always in pants or pant suits.  Over time I've been influenced by friends and family to appreciate fashion as an expression.  My fashion choices previously had been driven by my introverted nature and my lack of self confidence...using your choice of how you dress to express yourself is more important than you think.  Dress confidently- and you'll feel more confident!  We are all beautiful, and we deserve to own that.  Use your personal style to be a reflection of you.",
    "Current book/book you love?": "I¡¯m currently reading Lean In by Sheryl Sandburg \n\nIn terms of books that I love- I read anything by Dean Koontz and I love reading Robin CooneÿI like authors that have a science foundation to their writing.",
    "Favorite web site/blog/”guilty pleasure”/fun": "I read the NYTimes online to scan the headlines- it tends to be well rounded coverage of science, international  affairs and so on.",
    "Who/what inspires you?": "The thing that inspires me most are the incredible partnerships that I get the chance to be a part of!  Working with people to make our state a better place inspires me.  What tends to inspire me is inspirational people- the great work that I see people doing on the ground to make a difference.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": ""
  },
  {
    "Mentor Name": "reginaholliday",
    "name": "Regina Holliday",
    "Biography": "She has an A.B. in Politics/Economics from The Catholic University of America, Masters of Public Health in Maternal and Child Health and Ph.D. from the University of North Carolina at Chapel Hill and MBA from the Johnson School at Cornell University. Dr. Covington has authored numerous publications and is an impassioned public speaker. Much of her work focuses on addressing population disparities in health outcomes and cultural competency.",
    "What do you do every day?": "I work at the intersection of art and healthcare.  There is no reason why you need to wait to join healthcare!  Your voice is valuable- even right now!  I talk about national and global health policy, informatics, and I also paint about these things!  Health is about every part of our lives.",
    "Why do you love it?": "I love the intersection of art and health information technology because I love how new and open they were to different things.  That is really exciting for me, as an artist!",
    "What were your moments of fear/challenges in your career?": "I am sometimes in the position of being the only person in the room who is disruptive¡ªthe person who has to ask the tough questions.  I have to gather up the courage and do that, because it's important.",
    "What are some of the innovations in science that you are most excited about?": "Sensor technology¡ªnot just the fitness ones, but also self adhering heartbeat monitors or sensors in hospitals that help monitor patients without waking them up!",
    "Where did you grow up?": "Sapulpa, Oklahoma.",
    "Who was your favorite teacher and why?": "Mrs. Graham, in 4th grade, who created an individualized education plan for me and really designed a curriculum that matched my needs.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "I have the ability to paint about what I hear, in real time!",
    "Personal style/fashion tip? What’s in your purse?": "I don't carry a purse unless it is a costume prop.",
    "Current book/book you love?": "My favorite book is the Deed of Paksenarrion by Elizabeth Moon.  It is a fantasy book about a warrior for good.",
    "Favorite web site/blog/”guilty pleasure”/fun": "Cracked.com\n \nhilarious crowd sourced essays on weird news, history etc.  it's very far-reaching.",
    "Who/what inspires you?": "",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": ""
  },
  {
    "Mentor Name": "roseannstammen",
    "name": "Roseann Stammen",
    "Biography": "The daughter of Irish immigrants, I grew up in a working class family with four sisters.  We were taught to work hard, worship the Catholic Church and love yourself and your family.  I attended West Chester University and graduated with a BS in Business Administration.  I was able to intern at Merck & Co throughout college and was offered a full time position upon graduation.",
    "What do you do every day?": "I help physicians educate their patients on contraceptive options.",
    "Why do you love it?": "I love to empower women--they need to make informed decisions about family planning.",
    "What were your moments of fear/challenges in your career?": "The challenges in my career center around balancing work and life.  With two small children, it is a daily struggle to divide my time between work and home life.",
    "What are some of the innovations in science that you are most excited about?": "I'm always learning about new technologies and how they will impact my career.  I'm most excited about technologies in contraception and how they can increase compliance and convenience.",
    "Where did you grow up?": "Upper Darby, PA - it was a great town, with lots of wonderful neighbors.",
    "Who was your favorite teacher and why?": "Miss Adelizzi - she taught 3rd grade at St Laurence School in Upper Darby.  She was young, quirky and did things her way.  She taught us to think outside of the box and embrace differences.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "",
    "Personal style/fashion tip? What’s in your purse?": "Chap stick--I never leave home without it.  I always look better with a glossy lip.",
    "Current book/book you love?": "My favorite books are easy beach reads.  I love Jennifer Weiner, she writes about love, family and friendship - the cornerstones of life.",
    "Favorite web site/blog/”guilty pleasure”/fun": "",
    "Who/what inspires you?": "My parents, they came to America for a better life for their children.  Their courage to move thousands of miles from their home inspires me to be the best that I can be.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "My biggest hope is for my children.  I want to teach them to reach for their dreams, love themselves and take pride in who they are."
  },
  {
    "Mentor Name": "caseypierce",
    "name": "Casey Pierce",
    "Biography": "",
    "What do you do every day?": "Currently, I am a PhD candidate at Northwestern University in the Media, Technology and Society program in the School of Communication.  I really love my program because it takes an interdisciplinary approach to studying technology and its impacts on society. Specifically, I study how technologies are used in organizations for knowledge sharing, innovation and collaboration. In my dissertation research I examine how organizations use technologies to deal with new changes associated with healthcare policy reform. Because healthcare reform is such an important issue today with such significant consequences at stake, I am excited to research such a challenging and interesting topic.",
    "Why do you love it?": "I love research because I get to dive into questions that interest me. I get to travel the world for research and to attend conferences. I¡¯ve had the opportunities to visit India, London and all over the US as a doctoral student. I¡¯m looking forward to future trips to Asia and Europe. In addition to the perks of traveling, I also love the opportunities to meet and collaborate with smart people from different universities and research areas.",
    "What were your moments of fear/challenges in your career?": "The middle part my PhD program was rough for me, mostly because I questioned if I was ¡°good enough¡± to become a future professor and great researcher. My confidence overall was non-existent. I had a bad case of the ¡°imposter syndrome¡± where I felt that I was pretending to be smart enough when I was not. I constantly compared myself to others, which only made me feel bad about myself. I only focused on my weaknesses without giving due credit to my strengths.\n\nI eventually came to a point that I forced myself to stop thinking so negatively about my potential success. I reminded myself that I have overcome many challenges in my life _ the most difficult was losing my mother to cancer when I was 15 years old. After her passing, I not only had to deal with that deep personal grief, but also move states and change high schools in the middle of the school year. Now THAT was hard. Anyone who has been that ¡°new kid¡± at school can definitely relate! I thought, if I could go through that and make it through to the other side victoriously, I had no reason to fear whether I was good enough to excel in my PhD program. I now welcome challenges because I see them as opportunities to only improve and grow _ even if I am not perfect. Challenges do not have to hold you back with fear!",
    "What are some of the innovations in science that you are most excited about?": "I am excited to learn and research about the use of electronic medical records (EMRs) and electronic health records (EHRs). From my perspective as someone who studies technology and organizational change, I am interested how it changes the dynamics between the physician-patient relationship and how healthcare organizations can use EMRs and EHRs to improve the quality of care.",
    "Where did you grow up?": "I was born in Long Beach, California, but spent much of my years growing up in Long Island, NY and Norcross, Georgia. I finished out high school back in Palmdale, California and lived in Los Angeles when I attended USC for college. I eventually traded the SoCal weather when I moved to the great city of Chicago for graduate school. It¡¯s hard for me to pinpoint just one city as my hometown since each place had a unique impact on my life. However, having lived in some many places, my accent is more or less a blend of all the different regions!",
    "Who was your favorite teacher and why?": "Two of my elementary school teachers, Mrs. Hawk and Mrs. Hoover instilled the love of learning at such a young age. I also appreciate my junior high math teacher, Mr. Dimsdale, who motivated me to love math. Later on, in graduate school, I really loved taking classes with my professor, Andrea Hollingshead. She is not only an amazing researcher and scholar, but also a fantastic teacher. I would be remiss to not mention my current advisor and professor, Paul Leonardi, who was one of the main reasons I came to Northwestern. He has provided me with amazing opportunities and challenged me to do better work.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "Crafts! I especially love all things stationary. I love finding ways to ¡°upcycle¡± and re-purpose old things for new uses.",
    "Personal style/fashion tip? What’s in your purse?": "",
    "Current book/book you love?": "¡°When I Was Puerto Rican¡± by Esmeralda Santiago. I love reading memoirs, and I especially loved this book as I could relate to Santiago¡¯s experiences with culture, trying to fit in and finding one¡¯s identity.",
    "Favorite web site/blog/”guilty pleasure”/fun": "Hands down, the show ¡°24¡± is one of my faves. In my opinion, Jack Bauer is one of the best heroes of all time. When I have the time, I love to binge watch an entire series over a weekend.",
    "Who/what inspires you?": "My mom. She always pushed me to be different and not follow what everyone else was doing. Growing up I wanted to be so much like everyone else, but I now hold dear her philosophy to just be ¡°unashamedly me.¡± It definitely takes confidence and boldness, but life is so much more exciting following your own path rather than trying to fit in with the norm or other people¡¯s expectations.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": ""
  },
  {
    "Mentor Name": "inesdahne",
    "name": "Ines Dahne",
    "Biography": "My career began with a brief stint in IT and then I moved out to the sales force.  I have sold various therapeutic categories in my ten years as a Sales Representative including cardiovascular products, vaccines and now Women's Healthcare products.  Throughout my time at Merck, I was able to get my MBA in Marketing from St Joseph's University.",
    "What do you do every day?": "I work for one of the world's largest diagnostic laboratories. I lead an organization of 1,200 smart individuals who bring new diagnostic tests and IT solutions to the US and international healthcare marketplace.",
    "Why do you love it?": "I love it because I contribute to creating a healthier world every day and because I can get others excited about the difference that we can make.",
    "What were your moments of fear/challenges in your career?": "I don't find fear productive. Most challenges have occurred for me when I had a manager who had a personal agenda. I have learned and become a better leader through all my challenges.",
    "What are some of the innovations in science that you are most excited about?": "There are some proven ways to help patients adhere to treatment plans by playing online games. What's not exciting about computer games keeping us healthier?",
    "Where did you grow up?": "In East Germany in a former socialist country.",
    "Who was your favorite teacher and why?": "My first grade teacher. She named me class speaker. Without her, I would never have had the courage to speak up.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "Sticky situations usually have to do with people spending more time talking and less time listening.  An example of this is when developing a new product. I try to keep personal feelings out of the equation and find common ground.",
    "What is your unique talent? (can be something quirky)": "I smile all the time.",
    "Personal style/fashion tip? What’s in your purse?": "Check out http://www.bridgetteraes.com/. She has a great fashion blog that can help with any challenge. She insists one should spend 25% of your budget on accessories because fashion is like chicken - you need to spice it up! My purse holds enough to get me through an overnight camping trip. :)",
    "Current book/book you love?": "I love Cutting for Stone and Life of Pi. I currently read Brain on Fire.",
    "Favorite web site/blog/”guilty pleasure”/fun": "I travel to remote areas of the world and take photos. Expensive hobbies for sure.",
    "Who/what inspires you?": "I am inspired by anyone who finds and spreads joy, dignity and grace in all aspects of life and work.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "I  volunteer in Haiti and support sustainable business development. I try very hard to maintain my commitment to Haiti and not get too wrapped up in my career to help."
  },
  {
    "Mentor Name": "luciaregales",
    "name": "Lucia Regales",
    "Biography": "",
    "What do you do every day?": "I have scientific interactions and meetings with Doctors and Investigators in cancer. We discuss last advances, new therapies and findings in target molecular oncology drugs and how to improve the therapies.",
    "Why do you love it?": "Everyday I learn something new. The human genome started a new era in drug development. Everyday is different.",
    "What were your moments of fear/challenges in your career?": "When I was a postdoc fellow and I didn¡¯t get the expected results from some experiments. At First its confusing, but you just have to find the right answer for your result: Biology is not an exact science.",
    "What are some of the innovations in science that you are most excited about?": "Genome sequencing and immunotherapies. \nAll innovation related to personalized medicine.",
    "Where did you grow up?": "In Gijon, a Northern city of Spain, Europe.",
    "Who was your favorite teacher and why?": "My Biology teacher. He was very demanding, but I learnt a lot. He taught us how to love biology, which is life and how to respect it.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "I like to improve and optimize things. I was working with target therapies in a lung cancer mice model. We were getting stable disease response with most of the drugs we got. Based on different observations and experiments, I decided to combine two of them and then we got complete response and tumor shrinkage. That combination is now being used in a patient clinical trial.",
    "What is your unique talent? (can be something quirky)": "I am very science-sociable",
    "Personal style/fashion tip? What’s in your purse?": "I love jeans and spadriles sandals. I like to wear comfortable clothes. \nIn my purse, I always have a baby pacifier and a lip balm.",
    "Current book/book you love?": "One Hundred Years of Solitude- by Gabriel Garcia Marquez",
    "Favorite web site/blog/”guilty pleasure”/fun": "Scienceblog \nLinkedin",
    "Who/what inspires you?": "Hard strong working women: Marie Curie and my mother.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "I would like to support women in science and tell them that we can do a lot after we have our children or outside the bench. \nI would like to help women in their scientific career transition.\nAdditionally, I want to start a cancer integrative center in Spain."
  },
  {
    "Mentor Name": "jenniferasay",
    "name": "Jennifer Asay",
    "Biography": "Personally, I have been happily married to my husband, Tim, for five years and we have two small children.  We enjoy spending time with family, traveling and going to the beach every summer.  My life is busy with juggling various priorities in my work and my family life but I wouldn't change a thing :)",
    "What do you do every day?": "I work every day to help people live happier and healthier lives.  Regardless of the project, the patient is the reason why I work.",
    "Why do you love it?": "I love to help people and make life better for them and their families.",
    "What were your moments of fear/challenges in your career?": "One of the biggest fears I encountered was when I relocated my family for a role.  I've moved my family four times for my job so I was able to manage the fear.  The moves disrupted my children from their friends, family, schools, and extra curricular activities.  I was also concerned about my spouse's successful career and didn't want to harm him in anyway.  He was very supportive so it allowed us to move.",
    "What are some of the innovations in science that you are most excited about?": "I'm interested in the newest products to help people collect their own activity data (i.e. fit bit, basis, etc) to begin to address behavior change.  To help address the obesity and diabetes epidemics affecting the United States, these tools to help people with behavior change are critical and necessary.  The ability to passively monitor one's activity (steps, heart rate, sleep) and to collect the data into one place for evaluation is exciting and important.  There's still more work to do!  The current \"data capture\" tools are good, but can still be improved, especially regarding interconnectivity.  We then need to see more advancements in the field of behavioral science so our population can slow the epidemic.",
    "Where did you grow up?": "I grew up in a suburb in Indianapolis, Indiana.",
    "Who was your favorite teacher and why?": "Barbara Feringa - High School Chemistry teacher.  \nMrs. Feringa truly loved science and made it fun.  She was so supportive.  She encouraged me to participate in the science fair.  I'll never forget spending hours in the lab trying to grow penicillin.  I had so many issues with the agar in the plates.  I remember she asked me to participate in the science olympiad competition.  She did what she could with the equipment she had to help prepare us before the competition.  She was very flexible as I was an athlete as well and didn't have much time after school.  I remember walking into the competition lab and being shocked with the equipment that I was to use, but had never seen before.  She encouraged me to go outside my comfort zone, to try things not be afraid to fail, not panic and just try to come up with a solution.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "I'm a great bargain shopper.  I have a knack for finding things, typically at garage sales, of high quality for low prices.  While I don't get to do this very often anymore, I really enjoyed it.  It made me feel good to know that I was also recycling and helping the environment.",
    "Personal style/fashion tip? What’s in your purse?": "Wear comfortable heels.  Even though I'm tall, I wear heels at work.  So many years I'd wear whatever was \"cute\" but they might really hurt my feet.  I now will not compromise comfort for cuteness.  \n\nHair ties.  As soon as I leave the office, I often pull my hair back into a ponytail.",
    "Current book/book you love?": "I don't have time to read like I used to.  My current favorite book that I read frequently is \"I Love You Like Crazy Cakes\" by Rose Lewis.  It is a child's board book I read to my daughter at bedtime.  My husband and I adopted an infant from China in 2012.  It is one of the few books that speaks (lovingly) about Chinese adoption.",
    "Favorite web site/blog/”guilty pleasure”/fun": "People magazine - I rationalize reading this gossip magazine as I've actually created new ideas for patient benefit from reading articles or seeing certain advertisements.",
    "Who/what inspires you?": "Serving others inspires me.  Locally, within my state, or globally.  My family and I traveled to Swaziland to serve orphans in 2011.  It was an exhausting and exhiliarating experience.  I am an active volunteer with this organization to date.  Whenever I think things in my life are tough, I look at the photos of my friends (i.e. children orphans) in Swaziland who don't have daily clean water, regular food supply, a place to sleep, clothing, education or general safety).",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "I aspire to serve in a leadership capacity so I can help others achieve their potential.  When I retire, I expect I will run my own non-profit."
  },
  {
    "Mentor Name": "aprilleericsson",
    "name": "Aprille Ericsson",
    "Biography": "The majority of Dr. Ericsson¡¯s 20+ years engineering career has been at the NASA Goddard Space Flight Center (GSFC) in Applied Engineering & Technology Directorate (AETD). Initially she worked in the Guidance Navigation & Control discipline conducting spacecraft simulations and analysis to predict their dynamic behavior during flight and to determine the best spacecraft attitude and structural vibration control methods. Dr. Ericsson has also worked at NASA HQs as a Program Executive for the Earth Science Enterprise and a Resource Manager Space Science Enterprise. During the last 10 years, she has been an Instrument Manager (IM) in the GSFC Instrument Management and Systems Office. In this capacity, she has led/managed teams of scientist and engineers on various instrument proposals and flight missions. Her proposal efforts include: the Manager for the Space Science Small Explorer Advanced X-Ray Polarimeter (AXP) mission, which was awarded an unsolicited $0.5M to further develop its new technology; Telescope Manager for the Jupiter Magnetosphere Explorer; and, IM for the Vector ElectroDynamics Investigation, Terrestrial Planet Finder Coronagraph Spectrometer instrument (which won a $0.25M), and for Dust Collector Experiment on SCIM, a proposed Mars Scout sample and return mission. Additionally, Dr. Ericsson was the IM for NIRSpec Detector on the James Webb Space Telescope (a follow on mission to the Hubble Space Telescope) and the MMS SMART Fast Plasma Instrument suite. Un-characteristically of an engineer, Dr. Ericsson spent 5 months on detail as a Loaned Executive to the Combine Federal Campaign; there she was responsible for raising ~$2M from federal workers for charities across the Nation. Upon her return to GSFC, she was Project Engineer for a Technology development mission which would validate a miniature thermal loop heater/radiator system. Following that mission, she was the Project Engineer for Lunar Orbiter Laser Altimeter which launched April 2009, as one of the instruments aboard the Lunar Reconnaissance Orbiter.  LOLA provides topographic data to map the lunar surface in preparation for future moon exploration. As IM for the Gravity and Extreme Magnetism Small Explorer Dr. Ericsson lead the Instrument team through to selection as funded Small Explorer mission ($120M). For 3.5 years she served as the Deputy Instrument Project Manager for ICESat-2/ATLAS, a $480M lidar laser altimeter instrument that will provide mass and dimensional measurements over the Greenland and Antarctica ice sheets. Currently, Dr. Ericsson is the Deputy to the Chief Technologist of AETD with a particular focus on CubeSat and SmallSat Technology.",
    "What do you do every day?": "My jobs have changed at NASA- I am now the Deputy to Chief Technologist for our Applied Engineering and Technology Directorate.  My primary role is to expand the development of new technology for flight instruments.  I create partnerships using the resources we have while using our unique knowledge base.  Partners may include universities, companies, etc.",
    "Why do you love it?": "Every day- the challenges are different!  A lot of the times the challenges are people related- trying to inspire and get the best product delivered from our NASA workforce and providing the resources to solve the technical challenge.  The really cool thing is the developing technology- Currently, I'm focusing on really small satellites called CubeSats, that have the ability to fill the gap between a small budget, and great science.  I like that kind of challenge.  The science we support helps our communities- by understanding better our Earth, black holes, other planets, and the new knowledge we gain is really cool to me.",
    "What were your moments of fear/challenges in your career?": "I decided in the summer of my junior year that I wanted to do engineering- and I wanted to do it at MIT.  I went to a summer program my Algebra II teacher had recommended- Unfortunately, during my senior year of HS I crammed in science and math classes I needed before attending MIT...I didn't even have calculus before I got to MIT!  For the first time I was behind in math and science!  By my sophomore year of college, I had failed a class (twice!) - Differential equations!  Fortunately I had a great advisor at MIT who suggested I strengthen my understanding of the basics and re learn the math I needed- Following her suggestion I aced my final when I retook the class!  I didn't struggle anymore in engineering classes where math was a foundation.  This experience taught me about the ways to approach failure.  _There are ongoing struggles with when to change career paths, or market focus, or family focus, but if you build yourself a good support group, you can manage it all, with being a little flexible!",
    "What are some of the innovations in science that you are most excited about?": "CubeSats- it requires miniaturization of our instrumentations and spacecrafts- as you miniaturize the size of components that go on satellites, you bring down the cost.  If something is heavier and larger, it costs us more to put it in space.   So things like nano-manufacturing and compact electronics that work on a very small scale are exciting and that's where we are going in the future!",
    "Where did you grow up?": "Brooklyn, NY and Cambridge, MA- but I call Brooklyn my hometown- my mom's parents lived in Cambridge so I spent summers and high school and college there.",
    "Who was your favorite teacher and why?": "Sheila Widnall- first female Secretary of Defense, aero-fluid dynamics specialist _Dr. Wes Harris - he is an aeronautics specialist, and a mentor to me._Both at MIT",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "I can break down really complex technical information and break it down so anyone from any age groups and backgrounds can understand the concept.",
    "Personal style/fashion tip? What’s in your purse?": "I like to be comfortable- with a little bling!",
    "Current book/book you love?": "Sherlock Holmes- and I love all detective stories.  I liked trying to figure out the mystery before he did!  Today in my job, I feel like I get to do something similar.  Now as an adult, I like Stephen King- but they can be a little horrific.  _I really like poetry too- particularly Langston Hughes and Maya Angelou!",
    "Favorite web site/blog/”guilty pleasure”/fun": "Guilty pleasure- white chocolate!",
    "Who/what inspires you?": "Mae Jamison - first female astronaut_Tuskegee airmen _Dr. Neil deGrasse Tyson - he is an Astrophysicist narrates the Cosmos TV program and runs the Hayden Planetarium.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": ""
  },
  {
    "Mentor Name": "joycelee",
    "name": "Joyce Lee",
    "Biography": "Joyce Lee is  a pediatrician, associate professor, clinical health services researcher, and Social Media Editor for JAMA Pediatrics.  She specializes in diabetes, obesity, and the use of technology and social media.  She¡¯s interested in the notion that human centered design and design thinking combined with emerging technologies such as mobile technology, data visualization, and social media can transform the research enterprise and the delivery of clinical care. She co-directs the Program in Mobile Technology for Enhancing Child Health, which has the goal of creating mobile technology systems that can enhance chronic disease adherence in children, with a specific focus on adolescents with type 1 diabetes.\nDr. Lee is an Associate Professor at the University of Michigan in the School of Medicine¡¯s Pediatrics Department, and the School of Public Health¡¯s Environmental Sciences Department. She is one of a few individuals in the country who has completed dual training in Pediatric Health Services Research and Pediatric Endocrinology.  She obtained her Master in Public Health Degree from the University of Michigan¡¯s Department of Health Management and Policy.\nHer research agenda focuses on the epidemiology and health outcomes of childhood diabetes (type 1 and type 2) and the link between obesity and long-term endocrine consequences.  She is the principle investigator on several NIH-funded studies focusing on childhood obesity, linear growth, and on type 2 diabetes risk.  \nLee  was named a Brehm Investigator for Type 1 Diabetes Research and she is the site Principal Investigator for the University of Michigan for national diabetes registries including the Type 1 Diabetes Exchange and the Pediatric Diabetes Consortium.\nShe incorporates a variety of  methodologies, including cross-sectional and longitudinal epidemiologic analyses, transition state modeling techniques, agent based modeling techniques, applied clinical research, and cost-effectiveness analyses.",
    "What do you do every day?": "I write grants and papers, I give talks, I see patients, and I collaborate with a whole variety of individuals, like scientists, artists, and designers. I also mentor medical students, fellows, and junior faculty members.  Academia allows you to have the flexibility to pursue your ideas.",
    "Why do you love it?": "I love having the freedom to decide what I am want to work on.  No one is going to tell me what to pursue or study or who I should work with. I get to choose. And it's nice to know that you have the resources of a large university to draw on",
    "What were your moments of fear/challenges in your career?": "I think it's really easy to underestimate yourself; women tend to do this way more than men. Will I get that big grant? Will I get tenure? You have periods of self-doubt, but you have to power on through and know that you are worthy.",
    "What are some of the innovations in science that you are most excited about?": "I'm excited about patient centered design, DIY Health, and the role of social media for connecting the healthcare community. There's this online revolution happening under our screens.  Patients and caregivers are meeting and sharing ideas via social networks like Facebook and Twitter, and they are creating and sharing incredibly innovative and life-changing tools, technologies and solutions for their own disease community.",
    "Where did you grow up?": "Chicago, Illinois.  My dad was a pediatrician and so is my sister!",
    "Who was your favorite teacher and why?": "",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "",
    "Personal style/fashion tip? What’s in your purse?": "Always look your best.",
    "Current book/book you love?": "I love self-improvement websites- the Do Lectures, or 99U, or Lifehacker.",
    "Favorite web site/blog/”guilty pleasure”/fun": "Downton Abbey!",
    "Who/what inspires you?": "Design and designers inspire me. Design thinking is an approach that I am trying to use in my clinical, research and educational work. It's such an important skill to have as a physician and academic, to have the courage to fail many times before you find success. I enjoy following designers like Jessica Hische, who promotes the idea that you should pursue your own \"passion projects\".",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "I want to have more public impact with my work. I want to create systems, services, and products that actually improve the lives of our patients and families."
  },
  {
    "Mentor Name": "heidichumley",
    "name": "Heidi Chumley",
    "Biography": "Dr. Heidi Chumley is a family physician who joined AUC as Executive Dean and Chief Academic Officer on March 21, 2013. During her career, Dr. Chumley has focused on medical education, publishing educational research on topics including educational innovations and clinical reasoning. Dr. Chumley is one of the editors of The Color Atlas of Family Medicine, serves on the editorial board of Family Practice Essentials, a continuing medical education product produced by the American Academy of Family Physicians, and is a regular reviewer for Medical Teacher, an international journal focused on medical education. In her role as executive dean and chief academic officer, she is responsible for the oversight of the medical education program in its entirety.\nShe joined AUC following an eight-year career at the University of Kansas School of Medicine, where she most recently served as associate vice chancellor for educational resources and interprofessional education. Her responsibilities included fostering a vibrant learning environment supported by technology and other academic resources, as well as developing a center for interprofessional education and simulation. She served for nearly four years as senior associate dean for medical education, responsible for admissions, curriculum, and student affairs. Dr. Chumley also led initiatives in rural health, and cultural enhancement and diversity, while maintaining a full-scope family medicine practice that included delivering babies.\nDr. Chumley earned her medical degree from the University of Texas Health Science Center in San Antonio, where she also completed her residency in family medicine and a fellowship in academic leadership. From 1999 to 2004, she practiced in the University Health System in San Antonio. A native of Texas, Dr. Chumley received her bachelor¡¯s degree in biochemistry from Abilene Christian University.\nShe has been recognized with national awards for teaching, leadership, and scholarship, including the Parke Davis Award for Clinical Teaching, the Association of American Medical Colleges Early Career Women Faculty Professional Development Award, and numerous awards from the Society of Teachers of Family Medicine.",
    "What do you do every day?": "I¡¯m the dean of American University of the Caribbean School of Medicine. Being the dean is like being the principal of a school; it's all about ensuring that every student is successful and can move on to the next step. For medical students the next step is residency training in a medical specialty of their choosing.",
    "Why do you love it?": "I¡¯ve wanted to be a doctor since I was seven. After my own medical experience, I know that I wanted to make it better, especially for women. I really love my job because I feel like I get to make a difference.",
    "What were your moments of fear/challenges in your career?": "Training as a physician is incredibly challenging mentally, physically and emotionally.  However, you are still surrounded by mentors and friends who want to see you succeed. As I began my career in academic medicine, where I was a doctor and teaching future doctors, I saw that there were special challenges for women in academic medicine. I got married and raised a family, but this can be very challenging for someone with a career in academic medicine.",
    "What are some of the innovations in science that you are most excited about?": "Medicine is advancing every day, but while here are many affordable interventions that can help people, there are still parts of the population that don't have easy access to them. The opportunity to improve our system so that everyone has opportunities to access them is very exciting to me. I¡¯m also excited about the genomics revolution and I hope we can see genetic diseases eradicated.",
    "Where did you grow up?": "I grew up in Clear Lake Texas, halfway between Houston and Galveston near the Space Center. My mom is a teacher, and my dad works for IBM where he programmed for Apollo.",
    "Who was your favorite teacher and why?": "My favorite teacher was my high school basketball coach. I learned more about life from him than any of my other teachers. I learned how to be a teammate, how to stand for something important, how to be a leader, how to compete as a professional (be a good sport), and the importance of keeping your eye on the big picture (academic and personal growth).",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "",
    "Personal style/fashion tip? What’s in your purse?": "",
    "Current book/book you love?": "I love to read Malcolm Gladwell (The Tipping Point, David and Goliath, Blink). The way he sees the world and writes about it explains things very well. He sees that success is something we can drive ourselves. I have also been enjoying Tom Clancy novels. They are long, filled with intricate plots, and have a great historical background.",
    "Favorite web site/blog/”guilty pleasure”/fun": "My life is very hectic and it's intense at work and home. I¡¯m always busy. When I do have free time I love to go out on the beach, listen to the waves, and read a book. I need to find that peace to restore and refresh myself. If you lead a hectic, busy life, you need that so you can still have more to give.",
    "Who/what inspires you?": "Our medical students! Many of them at AUC come from difficult backgrounds and their stories are so incredible. They are extremely resilient, empathetic people and they become wonderful physicians because of their struggles and what they have had to overcome.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "Twenty years ago I kept saying I wanted to be the dean of a medical school and now I am! This is what I have wanted to do for a long time and I am enjoying it right now. On the horizon, I would like to have a higher level of involvement in health education policies globally. Right now, I'm having a lot of fun doing this!"
  },
  {
    "Mentor Name": "jehannineaustin",
    "name": "Jehannine Austin",
    "Biography": "Jehannine Austin is an Associate Professor in the Departments of Psychiatry and Medical Genetics at the University of British Columbia (UBC) in Vancouver, Canada, a Research Scientist at the BC Mental Health and Addictions Institute, and graduate advisor for the UBC Genetic Counseling program. She holds the Canada Research Chair in Translational Psychiatric Genomics. She completed her PhD in neuropsychiatric genetics at the University Of Wales College Of Medicine in Cardiff, UK, and her clinical training as a genetic counselor at UBC. Jehannine is board certified genetic counselor, and founded the world¡¯s first specialist psychiatric genetic counseling service of its kind in Vancouver, in 2012. Over the last 10 years, she has supervised a lot of students, enjoyed growing her clinical research team, and has held various leadership roles within the National Society of Genetic Counselors (the largest professional organization for genetic counselors in the world) and in 2013, received the organization's International Leader award. You can read more about her work here: http://psychiatry.ubc.ca/person/jehannine-austin/ and can follow her on twitter: @J9_Austin",
    "What do you do every day?": "I am a professor, researcher, and genetic counselor. No two of my days look the same, and that¡¯s something I really like about my job! My job entails writing grant applications to fund research projects that I am interested in. I write academic papers to share the results and the findings of the research our team has done. I spend a lot of time with students; many of whom are young women because genetic counseling is a female dominated field. I do a lot of public speaking and presenting about my work. There is also a clinical service aspect of my work - I oversee the running of the world¡¯s first psychiatric genetic counseling clinic.",
    "Why do you love it?": "My work is really all about trying to make what we know from research about the genetics of psychiatric disorders useful to people who have these conditions as well as their family members. That is interesting to me because there is a history of mental illness in my own family and I have had my own experiences with depression, so my area of research is very personally relevant. I am so passionate about my work because I can see the difference my research makes just about every day and that gives me huge amounts of pleasure. \n\nFor example, we do research studies where we are investigating what the effect is of providing genetic counseling for people who have mental illnesses like schizophrenia or bipolar disorder. When I am providing genetic counseling for one of our study participants and I can see it making a positive change for them in some way, perhaps it is making them feel less guilty about their illness or removing the stigma associated with their illness, that¡¯s hugely rewarding for me and will never get tiring. \n\nWriting grant applications and academic papers is a hugely creative process, and that¡¯s something I can actually lose hours in, enjoying the process of intellectual creativity. I also love interacting with my students and mentees. I have an amazing group of young women around me who are just full of the most incredible potential and I love helping them find their strengths and to grow in confidence and competence.",
    "What were your moments of fear/challenges in your career?": "I actually never wanted to be a professor. My PhD was all about identifying genetic variations that make a person more vulnerable to developing psychiatric illnesses, like schizophrenia or bipolar disorder. It was all very interesting research to me, but it was during my PhD that I learned that it wasn¡¯t personally satisfying to me. I didn¡¯t want to make a small contribution to a big change, which is the nature of basic science is all about. Essentially, I wanted to make a big change on a small scale. I wanted to witness the changes I was making; I wanted to be on the people end of things. PhD studies make you incredibly focused and have a deep knowledge, but I found that I didn¡¯t have the communication skills to describe how my research would be meaningful for people who had the disorders I was studying. So, that is what motivated me to train as a genetic counselor. When I finished my genetic counselling MSc training, I did not get the most receptive response trying to get hired as a psychiatric genetic counselor since not a lot of people were doing this very specific line of work. Also, there was a lot of scepticism about whether people with psychiatric illnesses wanted genetic counseling, and about the fact that there was little evidence that genetic counseling would be helpful for people with psychiatric illnesses. So I had to take a step back. I realized I had to do the research to find out whether people wanted genetic counseling or not, and if they did, was there anything positive that could come out this kind of interaction with a healthcare provider. Basically, that¡¯s how I ended up becoming a professor - through doing that research! \n\nI had an amazing mentor who was a psychiatrist who had never heard of genetic counseling before meeting me, but he saw the value in my work. He mentored me to write compelling grants, how to articulate my ideas clearly. Ultimately, I was able to win money from funding agencies to answer the sorts of research questions that I found interesting, and to generate evidence supporting the positive effects of genetic counseling for people with psychiatric illness. Through that process I ended up getting tenure as a professor and a prestigious national award a Canada research chair. This allowed me to create the specialist psychiatric genetic counsellor job that I had originally wanted when I graduated as a genetic counsellor -its just that I did not fill this job myself, instead, I hired a brilliant counselor to do it. I feel things have all worked out very well for me in the end - because I have found that I love my job as a professor. \n\nThe fear and challenge for me was confronting the idea of going back to a research role when at the time, after I had just graduated as a genetic counsellor, I wanted to be talking to people, I wanted to be in a service delivery role. I thought I didn¡¯t have it in me to withstand the competitive academic environment. I didn¡¯t think I was that clever or could survive in that culture. It scared me! In the first three years in my appointment as an assistant professor, I hated it. It was really hard. I did experience sexism. I experienced all sorts of unpleasant things, but what kept me going was my belief in what I was trying to do and help people. I continue to wrestle with ¡°imposter syndrome¡± that people will find out that I¡¯m actually not that clever, but that feeling becomes less and less over time. I remember when I was awarded the Canada research chair, I literally thought they made a mistake. Then when I realized it was in fact, intended for me, the pressure I felt to deliver was terrifying.",
    "What are some of the innovations in science that you are most excited about?": "I think there¡¯s always interesting things going on in the basic science fields, like finding genetic variations that contribute to all sorts of diseases. There¡¯s interesting work starting to come out that suggests we can modify our vulnerability to certain kinds of diseases. However, what I am most interested in is communicating with people who have illnesses about what basic science is finding about the causes of their conditions. I am very much interested in the people side of science. I want to take what basic hardcore, genetic, molecular scientists are finding in the lab and make that significant and meaningful for people that live with the conditions that are being researched. What gets me most fired up is about communication processes and how best to engage people. For example, one of the things we were very hopeful about with the human genome project, was how it would change our ability to treat and cure diseases. Now it is about 14 years since we had the first draft of the human genome and its impact on treating and curing diseases is limited. But, we have all of this knowledge about genetic variations that can contribute to the development of diseases, and I am interested in what we can do with that outside of curing disease, I am interested in figuring out how we best use what we know about the genetics of conditions together with counselling and communication skills to invoke behavior change in people. That¡¯s really what genetic counseling is all about _ it¡¯s not just about providing information, but providing information in a supportive and counseling based interaction.",
    "Where did you grow up?": "I was born in London (in the UK), but I did not grow up there. When I was about 8, my family moved to a seaside town in Wales called Swansea and I lived there until I was 18 when I moved to go away to university. Swansea is a beautiful place with green spaces and hills, but the implicit message I got at school was ¡°don¡¯t make too much of yourself¡± I felt that this was a particularly strong message if you were female. Many of the girls in my high school class had babies very young, even before we left high school, and did not go on to university. I did not feel that I was supported in fulfilling my potential.",
    "Who was your favorite teacher and why?": "Mrs. Moody, my high school math teacher, who was one of the few female math teachers that we had. She was my favourite because she made me feel like I could do it. In high school in the UK, you specialize in three subjects when you are 15. I decided to do chemistry, and biology but I didn¡¯t really know what to do for the third subject, so essentially because of Mrs. Moody I did math. She had confidence that I could do it and didn¡¯t treat girls with lower expectations, which is how I felt we were treated in other classes. She was actually quite inspirational to me. She spent time with us after class doing things like helping us to overcome our fears about doing math at a higher level.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "I have been a cave diver for the last ten years. That¡¯s essentially scuba diving in water filled caves. The caves I dive in are filled with fresh water and it is absolutely crystal clear. Because you are weightless, it feels like you are flying!",
    "Personal style/fashion tip? What’s in your purse?": "",
    "Current book/book you love?": "Where to start?! I have loads of favorite books. I love John Steinbeck, especially The Grapes of Wrath and I have read that three or four times. I also like Old Man in the Sea by Ernest Hemingway. Currently, I am reading ¡°Lean In,¡± by Sheryl Sandberg, which I have purchased for everyone on my team! I am totally geeking out on behavioral economics and everything about human decision making and how we think about things. The Invisible Gorilla, Nudge, Thinking Fast and Slow are all books I have recently read and loved.",
    "Favorite web site/blog/”guilty pleasure”/fun": "Well, its not really something I feel guilty about, but its something I am really enjoying right now, it is a twitter feed called the ¡°good men project.¡± It¡¯s like feminism for dudes. It is really cool and they talk about social pressures and expectations that are placed on men. It is very interesting because I have only had woman experiences, so it is interesting to think about other perspectives. There are really intelligent pieces posted on there that are really relevant to everyone - men and women.",
    "Who/what inspires you?": "I am inspired by the people around me.  I am inspired by watching my mentees grow and watching them get excited about the possibilities for what amazing things they will do next. I find the people with psychiatric disorders that I interact with in my clinic and in our research studies incredibly inspiring, they all seem incredibly brave especially given their willingness to share their experiences. I have had phenomenal mentors in my life who were truly altruistic in their wanting to help me grow for the sake of what I might be able to accomplish, not because of what it could do for them - and they continue to inspire me.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": ""
  },
  {
    "Mentor Name": "lisacooney",
    "name": "Lisa Cooney",
    "Biography": "Dr. Lisa Cooney is a licensed Marriage and Family Therapist, certified Access Consciousness Facilitator, and Master Theta Healer, she has supported thousands of people over the past 20 years in overcoming their childhood sexual abuse to create meaningful and joyful lives.\n \nDr. Lisa is no stranger to childhood sexual abuse. After her own traumatic childhood, she turned her life around in her 20¡¯s. Since then, she¡¯s gone on to create a comprehensive and cutting edge approach to her work with clients.\n \nAs an internationally sought out facilitator, speaker, and group leader, and author of the upcoming book, ¡°When Did You Become A Slave To Abuse? Getting Free in a New Way,¡± Dr. Lisa is known for using pragmatic tools to create quantum change.\n \nShe was the host of the radio show, ¡°The Psychology of Soul,¡± in which she interviewed well-known thought leaders such as Byron Katie. She was also interviewed on television on the topic of how individual healing impacts the collective.",
    "What do you do every day?": "A typical day starts with honoring myself and taking me time.  I exercise, or mediate, or set a target for my work day.  I usually start work at 10 o'clock with client appointments and business meetings.  I usually finish up at 6 pm with some me time.",
    "Why do you love it?": "Every single day I get to help people do better and be more confident.  I focus on helping people move past abuse through both my clinical background as a psychologist and my training as a marriage and family therapist.  I studied and focused on energy healing modalities and consciousness.  This combination helps people work through abuse to live a fulfilling life.  It's very satisfying.",
    "What were your moments of fear/challenges in your career?": "How do I go outside the traditional modalities and bridge that with the spiritual and energy modalities that I see as very prevalent today?  When I was in school, that wasn't as well known.  My fear was to be shunned by the clinical community while being embraced within the energy community.",
    "What are some of the innovations in science that you are most excited about?": "I'm really excited about a biological medicine tour I took in Europe.  I got to know some naturopathic doctors in the US that were working on thermographs. Thermometry is growing in scientific efficacy across the globe for an alternative wellness technology for Naturopathic medicine. The Thermometry machine is already approved in all of Europe and is awaiting FDA approval in the US. I am currently conducting a research study to show the efficacy of energy work on the body which shows there can be a change in chronic conditions through energy healing that is visually shown on the thermograph reading.",
    "Where did you grow up?": "",
    "Who was your favorite teacher and why?": "My favorite teacher was Judy Primavera.  I met her my senior year of college and she really made my senior year expansive and very healing for me.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "",
    "What is your unique talent? (can be something quirky)": "I have a unique ear for someones power and potency.  I really like to help people reach deep and get clarity so they can go on to live the life of their dreams.  I also have a unique talent for playing the drums!",
    "Personal style/fashion tip? What’s in your purse?": "I'm all about color!  Some colleagues of mine pointed out that I have a definite color palette; lots of blues, yellows, and greens!  It really spoke to feeling confident and dressing up, even for work!  The silkier the material, the better it feels on the body and the better you feel!",
    "Current book/book you love?": "Anita Moorjani¡ªher book on the afterworld and her change of perspective was though provoking.\nThe Five Love Languages.",
    "Favorite web site/blog/”guilty pleasure”/fun": "I love to travel!  I take vacations and I like going to different places all the time!",
    "Who/what inspires you?": "",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "I'm in the midst of creating my own thirteen week radio show on Radio Voice America and it¡¯s really exciting!  I also have a couple new tele seminars coming up too!"
  },
  {
    "Mentor Name": "joannakelly",
    "name": "Joanna Kelly",
    "Biography": "Dr. Joanna Kelley received her Bachelor of Arts in Mathematics and Biology with honors from Brown University in 2003. In 2008, she earned her Ph.D. in Genome Sciences from the University of Washington under advisor Professor Willie Swanson. Dr. Kelley did her postdoctoral training with Professor Molly Przeworski at the University of Chicago, where she received a National Institutes of Health Ruth L. Kirschstein National Research Service Award. She continued her postdoctoral training with Professor Carlos Bustamante in the Department of Genetics at Stanford University, where she received the 2012 L¡¯Oreal Fellowship for Women in Science. Dr. Kelley is currently an Assistant Professor in the School of Biological Sciences at Washington State University in Pullman, Washington. She was named one of the GenomeWeb Young Investigators in 2013.",
    "What do you do every day?": "I am a professor at Washington State University and my duties vary from day to day. I am typically working on at least two different projects within the laboratory.  A lot of what I do is computational so I'm at the computer often. I also teach Genome Sciences as well as Contemporary Genetics. I typically teach one class a semester.  I have my graduate degree, my PhD, in genome sciences. All of the research projects in my lab are around genetics and genomics.",
    "Why do you love it?": "I love genetics and genomics and science in general because I am able to experiment with  a lot of different questions and try to answer them. For me, doing research is really exciting. I love it because I'm always exploring new ideas and reading new things. I'm often reading journal articles and popular science articles to try and inform my own research on the latest and most interesting research.",
    "What were your moments of fear/challenges in your career?": "There have definitely been many challenging moments in my career. I actually started in college as a mathematics major. I loved mathematics through elementary school, high school, all throughout. I loved math all through my upbringing and then I reached a point where I thought maybe this isn't the right thing for me to do. That was a big challenge. Those debates on what classes to take, what steps to take, what track to take, were definitely a challenge but also very exciting.",
    "What are some of the innovations in science that you are most excited about?": "One of the latest innovations that is particularly close to me is the discovery of the thousand dollar genome. This is something that when I started graduate school, a number of years ago, never even existed; it was almost science-fiction.  Now we can genetically sequence the human genome with $1000 and that cost will go down in the next few years . This innovation really opens doors for the way we can look at human genetic data as well as other species. The fact that we can sequence the human genome gives us hope to sequence other species at low-cost to gain insight into biological processes. What's really exciting is the ability to sequence ancient genomes. Research on ancient genomes has been seen in many different articles.  There was one earlier last week about the frequency of different ancient genomes. It's really transforming the way we think about genetics and DNA¡ªIt's amazing!  One of my big projects for the PhD was looking at a specific thing that exists in tooth enamel formation. I¡¯ve spent a lot of time sequencing this gene and spent a lot of time in the lab.  Now this project can be done in less than a week. This proves how rapidly science technology is improving. All of these ideas are really revolutionizing genomics.",
    "Where did you grow up?": "I grew up in Santa Cruz, California. It was wonderful. I currently live in Pullman, Washington and it's snowing outside right now. Living in sunny California and going to high school 10 minutes from the beach was great.  The community in Santa Cruz is incredibly supportive and fun-loving and we were always outside.  I think that really improved my love of science, biology, and math¡ªjust the exposure playing in the woods, in the dirt, and constantly exploring.",
    "Who was your favorite teacher and why?": "One teacher that really influenced me in high school was actually the leadership teacher who also taught a leadership class. She really supported my leadership development and my ability to be involved in high school. This class didn¡¯t relate directly to science, it focused on my development as a leader, learning skills, and how to keep myself and  people organized. This definitely put me at an advantage even though it was a small scale thing. This was an opportunity for me to start as a leader and make small changes. Also when I was a graduate student there was a professor on my PhD committee who supported me. Her influence on my career has been incredible. She has been incredibly supportive and helped me maintain awareness of opportunities and how to take advantage of them.  She has also provided help regarding my research and pointing me towards people with similar interests. To this day she influences and supports my research. I feel very fortunate to have her as a supporter and a mentor.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "It's been very interesting adapting and learning the ways to run my own lab. This is very different than being a part of somebody else's research program, which had been my previous experience to this point. It's become apparent to me that [running a lab] it's kind of like running a small business. You have to learn how to manage money, and manage people, hire people, and train people while at the same time conducting research. It's not a specific interest where I need to change my approach but really just learning a whole new skill set for the job. It has been exciting, challenging, and interesting.",
    "What is your unique talent? (can be something quirky)": "One of my unique attributes is my enthusiasm. I am very excited about what I do, and it becomes very clear to anyone who works with me, which has lead to a lot of great collaborations and exciting discussions about science. My hope is that this enthusiasm becomes contagious.",
    "Personal style/fashion tip? What’s in your purse?": "",
    "Current book/book you love?": "My all time favorite book is called Rain of Gold by Victor Villasenor. It¡¯s a novel that¡¯s written about his parents and their immigration from Mexico to the US. It is a really beautiful novel about these two families and their challenges with coming across the border. Both of them, I believe, are undocumented and building their lives in the US.  Villasenor wonderfully illustrates how they meet, and how their lives become intertwined. I read it in middle school originally and I¡¯ve read it multiple times since then; I highly recommend it.",
    "Favorite web site/blog/”guilty pleasure”/fun": "For work, one of my favorite websites is twitter. Many people do not think about Twitter as a good resources for work but the scientific community that I am involved in has some pretty active posters and they¡¯re constantly contributing ideas, thoughts, and posting about new papers. For me its great to follow trending topics on a daily or weekly basis in science. That is a website that I use frequently to follow trends in genetics and populations genetics. For fun, prior to moving to Pullman when I actually lived closer to the water, I raced sailboats.  I started racing sailboats when I was a graduate student in Seattle and I have loved to be in the water racing ever since¡ªI¡¯ve become quite competitive. Now that I moved to Pullman and their isn¡¯t a big body of water I have spent time hiking and being outdoors but not on the water.",
    "Who/what inspires you?": "My biggest inspiration has been my parents¡ªmore specifically my mother. She has a PhD in biology and received it when very few women had a PhD in science. My parents have been continuously supportive, and pushing me and my siblings to accomplish whatever we can and always challenged us to do the best that we possibly could.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": ""
  },
  {
    "Mentor Name": "colleendodsonhonore",
    "name": "Colleen Dodson Honore",
    "Biography": "Colleen Dodson is a result focused executive with proven leadership and project management experience. Notable achievements include award winning market development, product launch experience, associate and advocate development and organizational change leadership. Skills and talents are seasoned with an appetite for learning, innovation, continuous improvement, and exceeding business objectives; flavored with an interpersonal flair and desire for collective success.",
    "What do you do every day?": "Well, I like to say I play multiple roles in life.  I¡¯ve been with the same company for 17 years (how time flies) and have held several roles throughout my career.  Currently, I am a member of a team that helps to improve the lives of people with diabetes. My role on this team is as Regional Business Director, which offers me the chance to lead a team of amazing people who focus on bringing valuable therapeutic options to patients in both the hospital and long-term care setting.  Another key role I play is as ¡°Mommy¡± to my four children (two are human the other two, canine!)",
    "Why do you love it?": "How couldn¡¯t I?  First, I work for an organization that has invested so much in my development and then has offered me a variety of opportunities over time to put these skills into action. During this journey, I have learned that my true talents are in building and leading strong teams which aligns to my life¡¯s purpose of inspiring others to see the beauty and possibilities in themselves. The role of a people leader offers me a huge platform to live out that purpose.  As a mom, my hope is to be an inspiration to my kids; to help them realize that anything in life is possible through faith, will, and determination. There are many barriers in life but the biggest ones are those we build in our mind. My wish for them is that they continue to be wonderful human beings and use their unique gifts and talents to contribute to our world in a positive way.  I couldn¡¯t ask for a better legacy.",
    "What were your moments of fear/challenges in your career?": "I think the biggest fear that I¡¯ve had in life is not being good enough.  Not being good enough professionally or personally.  As a child, my mom would say, ¡°Women have to work twice as hard to be considered half as good.¡±  That saying really stuck with me so throughout life I¡¯ve always worked extremely hard at everything so people would appreciate what I had to offer.  I have to admit, that can be exhausting! What I¡¯ve learned over time is that I¡¯ve always been good enoughÿI just needed to embrace that.  ¡°My best¡± is the best for me and instead of trying to always achieve others expectations of me, I needed to focus on exceeding my own expectations; which in fact, are much higher than those imposed by someone else.",
    "What are some of the innovations in science that you are most excited about?": "By far, human bionics and personal genomics.  My dad is the below the knee amputee from an accident and I¡¯ve grown up seeing the challenges that people face when they lose a limbÿboth physically and emotionally. Technology in the human bionics space has improved drastically over time and I am so encouraged by the progress we¡¯ve made and the promise that it holds. \nI am really fascinated by the concept of personal genomics.  Being able to understand my own DNA makeup and learn more about my lineage is so empowering and will allow me to make better choices regarding my own health.  I just bought a DNA kit that will allow me to explore the unknown within meÿhow cool is that!",
    "Where did you grow up?": "I was born and grew up on the south side of Chicago (Hyde Park).  I¡¯ve lived in a variety of places across the US and now find myself back where my roots started.  It¡¯s good to be home.",
    "Who was your favorite teacher and why?": "Ms. Borsdorfÿshe was my high school algebra teacher.  She was tough, but really good. She made me fall in love with math by sharing her secrets to being a great mathematician.  I still lean into her teachings.  I remember she used to say, ¡°What you¡¯ve do on one side of the equation, you have to do on the other.¡±  I still use this principle in both math and lifeÿit¡¯s all about balance.",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?": "First, let me just say that, in life, you can do your very best to avoid ¡°sticky¡± situations but sometimes they simply find you.  Once I took a position that was to serve as a stepping stone to another exciting opportunity soon thereafter.  However, what I learned very early on was that my new boss also held the same aspirations of wanting that other exciting role. It was a very uncomfortable situation at firstÿmy new boss and I potentially competing for the same job! I felt discouraged since I had left a role that I loved and could see that the assignments in my new position were not going to offer me the developmental opportunities to advance into the other role.  I really had to be still and not allow my anger to lead my decisions. I had to uncover what life was asking of me in this situation.  In time, I made the choice to make the best of my current role and did some pretty fun and amazing things which provided me other opportunities that I am now very grateful to have. As I reflect on this situation, I learned a valuable life¡¯s lessonÿit is not what happens in life that determines your success; it¡¯s what you make of it.",
    "What is your unique talent? (can be something quirky)": "I don¡¯t know if this is a unique talent or not but my aunt always told me I had a sixth sense.  My sense of intuition is extremely strong.  I can pick up on people¡¯s energies immediately and often hear the unspoken.  This gift has allowed me to develop a very strong emotional intelligence which has served me well in several aspects of my life.",
    "Personal style/fashion tip? What’s in your purse?": "Be you!  There is nothing more beautiful than people embracing who they really are.  While I love fashion especially a fabulous pair of shoes, inner peace coupled with self-assurance and gratitude, are always showstoppers in my book.  \nSince I travel a lot, I usually I carry floss picks, blotting tissue, and small bottle of cuticle oil in my purse at all times.  Clean teeth, matte skin and manicured ¡°looking¡± nails are a must!",
    "Current book/book you love?": "One of my favorite books is Man¡¯s Search for Meaning by Dr. Viktor Frankl.  This book changed me at my core. There are two lessons from this book that I carry with me each day. One is that I have the ability to choose how I want to respond to any situation. Between any stimulus and how I respond to it, I have a choice.  So often in life, we react. We allow our primitive responses to take over, like anger or frustration.  We don¡¯t take the opportunity to choose how we should respond.  In between a stimulus and my response, resides a space of choice.  I leverage that now more than ever. The second lesson I cherish is instead of asking, ¡°Why me¡± when something happens, I now ask, ¡°What is life asking of me in this situation.¡±  This shift in thinking prevents me from dwelling too long in personal sorrow and, instead, helps me to rise above my circumstance and be a better person because of it.",
    "Favorite web site/blog/”guilty pleasure”/fun": "My guilty pleasure is good game of Scrabble!  I especially love playing it on my iPad against the computer to challenge my skills.  I¡¯ve learned that it¡¯s not necessarily the length of a word you use that will render points, it the quality of the word.  How true is that in life as well!",
    "Who/what inspires you?": "My parents are so amazing.  They have always been my biggest fans and supporters.  They love me unconditionally and have been great role models all of my life.  Through good times and in bad they have shown me how to appreciate life and regardless of the situation, to be the very best person I can be.",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?": "I want to know that as well!  I have learned not to plan too much but to lean into what feels right.  As for now, I am where I should be from a career standpoint.  There¡¯s a lot of work to be done in my current role and when I feel like I¡¯ve completed what I¡¯ve been called to do, I will move on.  I am also married with two young children so this role offers me the professional challenge I desire, while also allowing me to be present with my family; which is very much a priority for me.  However, I am using this time to think about the next phase my life and how I can contribute to a greater degree."
  }
]

mentor_questions = [
    "What do you do every day?",
    "Why do you love it?",
    "What were your moments of fear/challenges in your career?",
    "What are some of the innovations in science that you are most excited about?",
    "Where did you grow up?",
    "Who was your favorite teacher and why?",
    "Who/what inspires you?",
    "What’s next for you?/What would you like to do when you “grow up’? (retire, etc.)/ what is something you hope to accomplish in the future?",
    "Describe an experience where you adapted your approach to resolve a “sticky” situation?",
    "What is your unique talent? (can be something quirky)",
    "Personal style/fashion tip? What’s in your purse?",
    "Current book/book you love?",
    "Favorite web site/blog/”guilty pleasure”/fun",
]

mentor_answers = [
    "carolgrieder,lead a team and manage outcomes,discover something new,yes,Yes,Yes,yes,no,no,Yes,work alone",
    "nganfhuang,work in a team and make things happen,discover something new,no,Yes,no,yes,yes,no,Yes,work in a group",
    "yolandabecker,lead a team and manage outcomes,discover something new,no,Yes,Yes,yes,yes,yes,Yes,work alone",
    "reshmasaujani,work in a team and make things happen,create something new,no,Yes,no,no,no,yes,no,work in a group",
    "annlindsay,lead a team and manage outcomes,create something new,yes,Yes,Yes,no,no,yes,Yes,work in a group",
    "lidiafonseca,lead a team and manage outcomes,create something new,yes,no,no,no,no,yes,no,work in a group",
    "andreamcgonigle,lead a team and manage outcomes,create something new,no,Yes,no,no,yes,no,no,work in a group",
    "laurepark,lead a team and manage outcomes,create something new,no,no,no,no,yes,no,Yes,work in a group",
    "sarahwamala,work in a team and make things happen,discover something new,no,no,no,no,no,no,no,work alone",
    "jeaninemartin,work in a team and make things happen,create something new,no,no,no,no,yes,no,no,work in a group",
    "akhilasatish,lead a team and manage outcomes,create something new,no,no,Yes,no,yes,yes,no,work alone",
    "lydiagreen,work in a team and make things happen,discover something new,no,no,no,no,no,no,no,work alone",
    "melvacovington,lead a team and manage outcomes,discover something new,yes,Yes,no,yes,no,yes,Yes,work in a group",
    "tanle,work in a team and make things happen,create something new,no,no,Yes,yes,yes,yes,Yes,work alone",
    "caoimhekiely,lead a team and manage outcomes,create something new,yes,no,no,no,no,yes,no,work in a group",
    "cristalthomas,work in a team and make things happen,discover something new,yes,Yes,Yes,yes,yes,no,no,work alone",
    "reginaholliday,lead a team and manage outcomes,create something new,no,Yes,no,no,no,yes,Yes,work alone",
    "roseannstammen,lead a team and manage outcomes,discover something new,no,Yes,no,no,no,no,no,work in a group",
    "caseypierce,lead a team and manage outcomes,create something new,yes,yes,no,no,yes,no,yes,work in a group",
    "inesdahne,lead a team and manage outcomes,create something new,no,no,no,no,no,no,Yes,work in a group",
    "luciaregales,lead a team and manage outcomes,discover something new,yes,no,no,yes,no,yes,no,work in a group",
    "jenniferasay,lead a team and manage outcomes,create something new,yes,no,yes,yes,yes,no,no,work in a group",
    "aprilleericsson,lead a team and manage outcomes,create something new,yes,Yes,Yes,yes,yes,yes,no,work alone",
    "joycelee,work in a team and make things happen,discover something new,yes,no,Yes,no,yes,no,Yes,work in a group",
    "heidichumley,lead a team and manage outcomes,discover something new,yes,no,Yes,yes,yes,no,no,work alone",
    "jehannineaustin,work in a team and make things happen,discover something new,no,no,no,yes,yes,no,no,work alone",
    "lisacooney,lead a team and manage outcomes,create something new,yes,Yes,Yes,no,no,no,Yes,work alone",
    "joannakelly,lead a team and manage outcomes,discover something new,yes,Yes,no,yes,yes,no,Yes,work in a group",
    "colleendodsonhonore,lead a team and manage outcomes,discover something new,no,Yes,no,yes,yes,no,no,work alone",
]

common_questions = [
    'At fifteen, I enjoyed:',
    'At fifteen, my favorite subjects were:',
    'I preferred:',
    'I preferred:',
    'I preferred:'
]


def load_mentors():
    for each_mentor in mentors:
        data = []
        c_ans = []
        global mentor_answers
        global mentor_questions
        global mentors
        global common_questions

        for each_question in mentor_questions:
            data.append([each_question, each_mentor[each_question]])

        for each_ans in mentor_answers:
            if each_mentor['Mentor Name'] in each_ans:
                for i in range(0, 6):
                    for q_1 in ['Drawing', 'Writing', 'Painting', 'Sports', 'Going to the theater', 'Being outdoors', 'Exploring/traveling', 'Playing with animals']:
                        if q_1.lower() in each_ans.lower():
                            c_ans.append([str(common_questions[0]), q1])
                            break

                    for q_2 in ['Math', 'History', 'Biology', 'Chemistry', 'English']:
                        if q_2.lower() in each_ans.lower():
                            c_ans.append([str(common_questions[1]), q2])
                            break

                    for count, q_3 in enumerate(['Work alone', 'Work in a group']):
                        q3a = ['Working alone', 'Working in a group']
                        if q_3.lower() in each_ans.lower():
                            c_ans.append([str(common_questions[2]), q3a[count]])
                            break

                    for count, q_4 in enumerate(['Create something new','Discover something new']):
                        q4a = ['Creating something new','Discovering something new']
                        if q_4.lower() in each_ans.lower():
                            c_ans.append([str(common_questions[3]), q4a[count]])
                            break

                    for count, q_5 in enumerate(['Work in a team and make things happen', 'Lead a team and manage outcomes']):
                        q5a = ["Working in a team", "Leading a team"]
                        if q_5.lower() in each_ans.lower():
                            c_ans.append([str(common_questions[4]), q5a[count]])
                            break

        img = open('./media/userpics/' + str(each_mentor['Mentor Name']) + '.jpg', 'rb')
        jpgdata = img.read()
        img.close()

        jpgdata = 'data:;base64,' + b64encode(jpgdata).decode()

        UserProfile.objects.create(
            bio=each_mentor['Biography'],
            name=each_mentor['name'],
            image=jpgdata,
            user=User.objects.create_user(
                username=each_mentor['Mentor Name'],
                email=each_mentor['Mentor Name'] + '@gmail.com',
                password=each_mentor['Mentor Name']
            ),
            other_answers=data,
            common_answers=c_ans,
            signup_type=2
        )


def match_mentor(user):
    all_role_models = UserProfile.objects.filter(signup_type=2)
    current_user = UserProfile.objects.filter(user=user)

    current_user_answer = current_user[0].common_answers
    current_user_answer = [x[1].lower() for x in current_user_answer]

    match = None
    if all_role_models:
        ind = random.randrange(0, len(all_role_models))
        match = all_role_models[ind]

    best_score = 0

    for each_user in all_role_models:
        mentor_answers = each_user.common_answers
        mentor_answers = [x[1].lower() for x in mentor_answers]

        if not mentor_answers:
            continue

        current_best = 0
        for (a, b) in zip(current_user_answer, mentor_answers):
            if a == b:
                current_best += 1

        if current_best > best_score:
            best_score = current_best
            match = each_user


    Mentors.objects.get_or_create(
        girl=current_user[0],
        mentor=match
    )

    return match


class ProfileLoad(TemplateView):
    """Home page for students."""
    template_name = 'pages/index.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        load_mentors()
        return render(request, self.template_name, {'home': True})

class RoleProfile(TemplateView):
    """docstring for RoleProfile"""
    template_name = 'pages/rolemodels.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        rolemodels = UserProfile.objects.filter(signup_type=2, user__is_active=True)
        for each_rolemodels in rolemodels:
            each_rolemodels.image = each_rolemodels.image

        return render(request, self.template_name, {'rolemodels': rolemodels, 'tab': 'role'})    
        
class HomeView(TemplateView):
    """Home page for students."""

    template_name = 'pages/index.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        if request.user.is_authenticated and request.user.is_superuser:
            return HttpResponseRedirect('/admin/')
        elif request.user.is_authenticated:
            return HttpResponseRedirect('/quiz/')
        return render(request, self.template_name, {'home': True, 'tab': 'home'})


class AboutView(TemplateView):
    """Home page for students."""

    template_name = 'pages/about.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        return render(request, self.template_name, {'tab': 'about'})


class ApproveAccount(TemplateView):
    """Home page for students."""

    template_name = 'pages/approve.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        rolemodels = UserProfile.objects.filter(signup_type=2, user__is_active=False)
        return render(request, self.template_name, {'models': rolemodels})


class ContactView(TemplateView):
    """Home page for students."""

    template_name = 'pages/contact.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        return render(request, self.template_name, {'tab': 'contact'})


class MailView(TemplateView):
    """Home page for students."""

    template_name = 'pages/thanks.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        # q1 = request.args
        # email = q1['comments']
        # if email!='':
        # write_log_file(MAILING_LIST, email)
        # return render_template('thanks.html')
        return render(request, self.template_name, {})


class MissionView(TemplateView):
    """Home page for students."""

    template_name = 'pages/misssion.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        # q1 = request.args
        # email = q1['comments']
        # if email!='':
        # write_log_file(MAILING_LIST, email)
        # return render_template('thanks.html')
        return render(request, self.template_name, {'tab': 'mission'})


class GalleryView(TemplateView):
    """Home page for students."""

    template_name = 'pages/gallery.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        # mk = links.keys()
        # random.shuffle(mk)
        # return render_template('gallery.html', images = mk[:16], profiles = profiles)
        return render(request, self.template_name, {})


class ProfileActivationView(TemplateView):
    """Home page for students."""

    template_name = 'pages/activate.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        return render(request, self.template_name, {})


class QuizView(TemplateView):
    """Quiz page for students."""

    template_girls = 'pages/survey_girls.html'
    template_models = 'pages/survey_models.html'

    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        try:
            userprof = UserProfile.objects.get(user=request.user)
        except:
            username = request.session.get('username', '')
            if username:
                userprof = UserProfile.objects.get(user__username=username)
            else:
                return HttpResponseRedirect('/')

        mentors = Mentors.objects.filter(girl=userprof)
        common_len = 0
        if userprof.common_answers:
            common_len = len(userprof.common_answers)

        if common_len > 0 and userprof.signup_type == 2:
            return HttpResponseRedirect('/profile/match/')
        elif common_len > 0 and userprof.signup_type == 1:
            return HttpResponseRedirect('/profile/match/')
        else:
            if userprof.signup_type == 1:
                # questions = load_questions("questions_final.csv")
                return render(request, self.template_girls, {})
            else:
                return render(request, self.template_models, {})

class ConnectionView(TemplateView):
    template = 'pages/connections.html'

    def get(self, request, profile_id, *args, **kwargs):
        """Method for get request of home page."""
        userprof = UserProfile.objects.get(id=int(profile_id))
        userprof.image = userprof.image
        if userprof.user.id != request.user.id:
            return HttpResponseRedirect('/')

        all_connected_girls = Mentors.objects.filter(mentor__id=int(profile_id))

        for each_conn in all_connected_girls:
            if each_conn.girl:
                each_conn.girl.image = each_conn.girl.image
            if each_conn.mentor:
                each_conn.mentor.image = each_conn.mentor.image

        return render(
            request,
            self.template,
            {
                'connections': all_connected_girls,
                'userprof': userprof
            }
        )
        

class ResultView(TemplateView):
    """Home page for students."""

    template_name = 'pages/profile.html'

    def post(self, request, *args, **kwargs):
        """Method for get request of home page."""
        try:
            userprof = UserProfile.objects.filter(user=request.user)
        except:
            username = request.session.get('username', '')
            if username:
                userprof = [UserProfile.objects.get(user__username=username)]

        myprofile = userprof[0]
        myprofile.image = myprofile.image
        name = request.POST.get('name', '')
        linkedin = request.POST.get('linkedin', '')
        bio = request.POST.get('bio', '')

        common_answer = []
        role_answer = []

        global common_questions
        common_questions_length = len(common_questions)
        
        for i in range(0, common_questions_length):
            ans = request.POST.get('common' + str(i + 1), '')
            common_answer.append([common_questions[i], ans])

        global mentor_questions
        role_models_questions_length = len(mentor_questions)

        if myprofile.signup_type == 2:
            for i in range(0, role_models_questions_length):
                ans = request.POST.get('question' + str(i + 1))
                role_answer.append([mentor_questions[i] , ans])

        if name != '':
            myprofile.name = name

        myprofile.common_answers = common_answer
        myprofile.other_answers = role_answer

        if linkedin != '':
            myprofile.linkedin = linkedin

        myprofile.bio = bio
        myprofile.save()

        if myprofile.user.is_active:
            return HttpResponseRedirect('/profile/match/')
        else:
            return HttpResponseRedirect('/profile/activation/')


class GirlProfileView(TemplateView):
    """docstring for GirlProfileView"""
    template_name = 'pages/girlprofile.html'    
    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        profile_id = self.kwargs.get('profileid')
        userprof = UserProfile.objects.get(id=int(profile_id))
        if userprof:
            userprof.image = userprof.image
        return render(
            request,
            self.template_name,
            {
                'girl': userprof
            }
        )
        

class ProfileView(TemplateView):
    """Home page for students."""

    template_name = 'pages/profile.html'

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            profile_id = self.kwargs.get('profileid')
            mentors = UserProfile.objects.filter(id=int(profile_id))
            mentor = mentors[0]

            mentor.user.is_active = True
            mentor.user.save()
            if mentor:
                mentor.image = mentor.image
            return render(
                request,
                self.template_name,{'mentor': mentor}
            )


    def get(self, request, *args, **kwargs):
        """Method for get request of home page."""
        if request.user.is_superuser:
            profile_id = self.kwargs.get('profileid')
            mentors = UserProfile.objects.filter(id=int(profile_id))
            mentor = mentors[0]
            if mentor:
                mentor.image = mentor.image
            return render(
                request,
                self.template_name,{'mentor': mentor}
            )

        userprof = UserProfile.objects.get(user=request.user)
        userprof.image = userprof.image
        # mentor = match_mentor(request.user)
        if userprof.signup_type == 1:
            mentors = Mentors.objects.filter(girl=userprof)
            if len(mentors) == 0:
                mentor = match_mentor(request.user)
                if mentor:
                    mentor.image = mentor.image
            else:
                mentor = mentors[0].mentor
                if mentor:
                    mentor.image = mentor.image

            return render(
                request,
                self.template_name,
                {
                    'mentor': mentor,
                    'userprof': userprof
                }
            )
        else:
            girls = Mentors.objects.filter(mentor=userprof)
            for each_g in girls:
                each_g.girl.image = each_g.girl.image

            return render(
                request,
                self.template_name,
                {
                    'girls': girls,
                    'mentor': userprof,
                    'userprof': userprof
                }
            )
