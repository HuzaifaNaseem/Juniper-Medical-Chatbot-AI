"""
Medical Knowledge Base
Comprehensive embedded medical information for RAG system
No external files required - all data is self-contained
"""

MEDICAL_KNOWLEDGE = [
    # ==========================================
    # CARDIOVASCULAR DISEASES
    # ==========================================
    {
        "title": "Hypertension (High Blood Pressure)",
        "category": "cardiovascular",
        "content": """
Hypertension, or high blood pressure, is a chronic medical condition where blood pressure in the arteries is persistently elevated.
Blood pressure is measured in millimeters of mercury (mmHg) and recorded as two numbers: systolic pressure (when the heart beats)
over diastolic pressure (when the heart rests between beats). Normal blood pressure is below 120/80 mmHg.

Hypertension is diagnosed when readings consistently show 130/80 mmHg or higher. It's often called the "silent killer" because
it typically has no symptoms until it causes significant damage to organs.

Risk Factors: Age, family history, obesity, excessive salt intake, lack of physical activity, tobacco use, chronic stress,
kidney disease, diabetes, and sleep apnea.

Complications: If left untreated, hypertension can lead to heart attack, stroke, heart failure, kidney damage, vision problems,
peripheral artery disease, and cognitive impairment.

Treatment: Lifestyle modifications (diet, exercise, weight loss, stress reduction) and medications including ACE inhibitors,
beta-blockers, calcium channel blockers, diuretics, and angiotensin II receptor blockers (ARBs). Regular monitoring is essential.
"""
    },
    {
        "title": "Coronary Artery Disease (CAD)",
        "category": "cardiovascular",
        "content": """
Coronary Artery Disease is the most common type of heart disease and the leading cause of death worldwide. CAD occurs when
the coronary arteries, which supply blood to the heart muscle, become narrowed or blocked by atherosclerotic plaques.

Atherosclerosis is the buildup of cholesterol, fat, calcium, and other substances in the arterial walls, forming plaques that
restrict blood flow. When blood flow to the heart muscle is reduced, it can cause chest pain (angina). Complete blockage can
trigger a heart attack (myocardial infarction).

Symptoms: Chest pain or discomfort (angina), shortness of breath, fatigue, heart palpitations, pain in the neck, jaw, throat,
upper abdomen, or back. Some people have no symptoms until a heart attack occurs.

Risk Factors: High cholesterol, high blood pressure, diabetes, smoking, obesity, physical inactivity, family history, age,
and chronic stress.

Diagnosis: ECG, stress testing, echocardiography, coronary angiography, CT coronary angiogram, and blood tests including
lipid profiles and cardiac biomarkers.

Treatment: Lifestyle changes, medications (statins, aspirin, beta-blockers, ACE inhibitors), angioplasty with stent placement,
or coronary artery bypass grafting (CABG) surgery in severe cases.
"""
    },
    {
        "title": "Heart Failure",
        "category": "cardiovascular",
        "content": """
Heart failure is a chronic progressive condition where the heart muscle doesn't pump blood as well as it should. Despite its name,
heart failure doesn't mean the heart has stopped working entirely—it means the heart is working less efficiently than normal.

Types: Systolic heart failure (reduced ejection fraction) occurs when the heart muscle doesn't contract effectively. Diastolic
heart failure (preserved ejection fraction) occurs when the heart muscle is stiff and doesn't fill properly.

Causes: Coronary artery disease, heart attack, high blood pressure, heart valve disease, cardiomyopathy, congenital heart defects,
viral infections affecting the heart, and chronic conditions like diabetes and obesity.

Symptoms: Shortness of breath during activity or while lying down, fatigue, weakness, swelling in legs and ankles (edema),
rapid or irregular heartbeat, persistent cough or wheezing with white or pink blood-tinged phlegm, increased need to urinate
at night, abdominal swelling, sudden weight gain from fluid retention, lack of appetite, nausea, and difficulty concentrating.

Treatment: Medications (ACE inhibitors, beta-blockers, diuretics, aldosterone antagonists, digoxin), lifestyle modifications
(salt restriction, fluid management, exercise), implanted devices (pacemakers, defibrillators), and in severe cases,
heart transplantation or ventricular assist devices.
"""
    },

    # ==========================================
    # DIABETES & ENDOCRINE DISORDERS
    # ==========================================
    {
        "title": "Type 1 Diabetes",
        "category": "endocrine",
        "content": """
Type 1 diabetes is an autoimmune condition where the body's immune system attacks and destroys the insulin-producing beta cells
in the pancreas. Without insulin, glucose cannot enter cells and builds up in the bloodstream, leading to hyperglycemia.

Type 1 diabetes typically develops in children and young adults, though it can occur at any age. It accounts for about 5-10%
of all diabetes cases and requires lifelong insulin therapy.

Pathophysiology: The exact cause is unknown, but it involves a combination of genetic susceptibility and environmental triggers
(possibly viral infections). The autoimmune destruction of beta cells leads to absolute insulin deficiency.

Symptoms: Increased thirst and urination, extreme hunger, unintended weight loss, fatigue, irritability, blurred vision,
slow-healing sores, and frequent infections. Symptoms often develop quickly over weeks or months.

Complications: Diabetic ketoacidosis (DKA), cardiovascular disease, nerve damage (neuropathy), kidney damage (nephropathy),
eye damage (retinopathy), foot damage, skin conditions, hearing impairment, and cognitive difficulties.

Treatment: Multiple daily insulin injections or insulin pump therapy, continuous glucose monitoring, carbohydrate counting,
regular blood glucose monitoring, healthy diet, regular exercise, and management of complications. The goal is maintaining
HbA1c levels below 7% for most adults.
"""
    },
    {
        "title": "Type 2 Diabetes",
        "category": "endocrine",
        "content": """
Type 2 diabetes is a chronic metabolic disorder characterized by insulin resistance and relative insulin deficiency. Unlike
Type 1, the pancreas still produces insulin, but the body's cells don't respond properly to it, and over time, the pancreas
may not produce enough insulin to maintain normal glucose levels.

Type 2 diabetes accounts for 90-95% of all diabetes cases and typically develops in adults over 45, though increasing rates
are seen in younger individuals due to rising obesity rates.

Risk Factors: Obesity, physical inactivity, family history, age over 45, gestational diabetes history, polycystic ovary
syndrome (PCOS), prediabetes, high blood pressure, abnormal cholesterol levels, and certain ethnicities (African American,
Hispanic, Native American, Asian American, Pacific Islander).

Symptoms: Increased thirst and urination, increased hunger, fatigue, blurred vision, slow-healing wounds, frequent infections,
numbness or tingling in hands or feet, and areas of darkened skin (acanthosis nigricans). Symptoms develop gradually and may
be mild initially.

Prevention: Weight management, healthy eating (Mediterranean diet, low glycemic index foods), regular physical activity
(150 minutes per week), smoking cessation, and blood pressure/cholesterol control.

Treatment: Lifestyle modifications (diet, exercise, weight loss), oral medications (metformin, sulfonylureas, DPP-4 inhibitors,
SGLT2 inhibitors, GLP-1 agonists), injectable medications (insulin, GLP-1 receptor agonists), and regular monitoring of blood
glucose and HbA1c levels.
"""
    },
    {
        "title": "Hypothyroidism",
        "category": "endocrine",
        "content": """
Hypothyroidism is a condition where the thyroid gland doesn't produce enough thyroid hormones (T3 and T4). These hormones
regulate metabolism, energy production, body temperature, heart rate, and many other vital functions.

The most common cause worldwide is iodine deficiency. In developed countries, Hashimoto's thyroiditis (an autoimmune disorder)
is the leading cause. Other causes include thyroid surgery, radiation therapy, certain medications, and pituitary disorders.

Symptoms: Fatigue, weight gain, cold intolerance, constipation, dry skin, hair loss, muscle weakness, elevated cholesterol
levels, depression, impaired memory, slowed heart rate, puffy face, hoarse voice, and menstrual irregularities in women.

Diagnosis: Blood tests measuring TSH (thyroid-stimulating hormone) and free T4 levels. Elevated TSH with low T4 indicates
primary hypothyroidism. Thyroid antibody tests can identify autoimmune causes.

Treatment: Levothyroxine (synthetic T4) is the standard treatment. Dosing is individualized based on TSH levels, age, weight,
cardiovascular status, and other factors. Regular monitoring ensures optimal dosing. Treatment is typically lifelong.

Complications if untreated: Goiter, heart problems, peripheral neuropathy, myxedema (severe hypothyroidism), infertility,
and birth defects if occurring during pregnancy.
"""
    },

    # ==========================================
    # RESPIRATORY DISEASES
    # ==========================================
    {
        "title": "Asthma",
        "category": "respiratory",
        "content": """
Asthma is a chronic inflammatory disorder of the airways characterized by variable and recurring symptoms, reversible airflow
obstruction, bronchospasm, and airway hyperresponsiveness. During an asthma attack, the airways become inflamed, muscles around
them tighten, and mucus production increases, making breathing difficult.

Types: Allergic asthma (triggered by allergens), non-allergic asthma (triggered by stress, exercise, cold air, smoke),
occupational asthma (workplace irritants), exercise-induced bronchoconstriction, and aspirin-exacerbated respiratory disease.

Triggers: Airborne allergens (pollen, dust mites, mold, pet dander), respiratory infections, physical activity, cold air,
air pollutants, certain medications (beta-blockers, aspirin), stress, sulfites and preservatives in food, and GERD.

Symptoms: Shortness of breath, chest tightness or pain, wheezing when exhaling, trouble sleeping due to shortness of breath,
coughing or wheezing attacks worsened by respiratory viruses, and variability in symptoms over time and intensity.

Diagnosis: Medical history, physical examination, lung function tests (spirometry, peak flow measurement), allergy testing,
chest X-ray, and exhaled nitric oxide test.

Treatment: Quick-relief medications (short-acting beta-agonists like albuterol), long-term control medications (inhaled
corticosteroids, long-acting beta-agonists, leukotriene modifiers, biologics for severe asthma), trigger avoidance,
asthma action plan, and regular monitoring with peak flow meter.
"""
    },
    {
        "title": "Chronic Obstructive Pulmonary Disease (COPD)",
        "category": "respiratory",
        "content": """
COPD is a progressive lung disease that causes obstructed airflow from the lungs. It includes emphysema (damage to air sacs)
and chronic bronchitis (long-term inflammation of airways). COPD is primarily caused by long-term exposure to irritating
gases or particulate matter, most often from cigarette smoke.

Pathophysiology: In emphysema, alveoli are destroyed, reducing the lung's surface area for gas exchange. In chronic bronchitis,
airways become inflamed and narrowed, producing excessive mucus. Most COPD patients have both conditions.

Symptoms: Increasing breathlessness (especially during activities), persistent chesty cough with phlegm, frequent chest infections,
persistent wheezing, fatigue, weight loss (in advanced stages), and swelling in ankles.

Risk Factors: Tobacco smoking (primary cause), occupational exposure to dust and chemicals, indoor air pollution (biomass fuel),
alpha-1 antitrypsin deficiency (genetic factor), and history of childhood respiratory infections.

Diagnosis: Spirometry (measures FEV1/FVC ratio), chest X-ray or CT scan, arterial blood gas analysis, and alpha-1 antitrypsin
deficiency screening.

Treatment: Smoking cessation (most important), bronchodilators (short and long-acting), inhaled corticosteroids, combination inhalers,
phosphodiesterase-4 inhibitors, theophylline, pulmonary rehabilitation, oxygen therapy, and in severe cases, surgery
(lung volume reduction or transplantation). Vaccinations (flu, pneumococcal) are important for prevention of exacerbations.
"""
    },
    {
        "title": "Pneumonia",
        "category": "respiratory",
        "content": """
Pneumonia is an infection that inflames the air sacs in one or both lungs, which may fill with fluid or pus. It can range from
mild to life-threatening and is most serious for infants, young children, people over 65, and people with weakened immune systems.

Types: Community-acquired pneumonia (most common type), hospital-acquired pneumonia (develops during hospital stay),
healthcare-associated pneumonia, ventilator-associated pneumonia, and aspiration pneumonia.

Causes: Bacteria (Streptococcus pneumoniae most common), viruses (influenza, RSV, COVID-19), fungi (in immunocompromised),
and mycoplasma (walking pneumonia). Pathogens vary by age, immune status, and exposure.

Symptoms: Chest pain when breathing or coughing, cough with phlegm or pus, fatigue, fever with sweating and chills, lower than
normal body temperature (in older adults), nausea and vomiting, shortness of breath, confusion (especially in elderly).

Diagnosis: Physical examination (listening for abnormal breath sounds), chest X-ray, blood tests, sputum culture, pulse oximetry,
CT scan, pleural fluid culture (if effusion present), and bronchoscopy in complicated cases.

Treatment: Bacterial pneumonia treated with antibiotics; viral pneumonia may require antiviral medications. Supportive care
includes fever reducers, cough medication, rest, and fluids. Hospitalization may be needed for severe cases, elderly patients,
or those with underlying conditions. Prevention includes pneumococcal and influenza vaccines.
"""
    },

    # ==========================================
    # INFECTIOUS DISEASES
    # ==========================================
    {
        "title": "Influenza (Flu)",
        "category": "infectious",
        "content": """
Influenza is a contagious respiratory illness caused by influenza viruses that infect the nose, throat, and sometimes the lungs.
It can cause mild to severe illness and can lead to hospitalization or death, especially in high-risk groups.

Types: Influenza A (causes seasonal epidemics and pandemics, infects humans and animals), Influenza B (causes seasonal epidemics,
primarily infects humans), Influenza C (causes mild respiratory illness), and Influenza D (primarily affects cattle).

Transmission: Spreads through respiratory droplets when infected people cough, sneeze, or talk. Can also spread by touching
contaminated surfaces then touching mouth, nose, or eyes. People are most contagious in the first 3-4 days after illness begins.

Symptoms: Sudden onset of fever, chills, cough, sore throat, runny or stuffy nose, muscle or body aches, headaches, fatigue,
and sometimes vomiting and diarrhea (more common in children). Distinguishing from common cold: flu symptoms are more severe
and have sudden onset.

Complications: Pneumonia (bacterial or viral), bronchitis, sinus infections, ear infections, myocarditis, encephalitis,
multi-organ failure, sepsis, and worsening of chronic medical conditions (asthma, heart disease, diabetes).

Prevention: Annual flu vaccination (most effective preventive measure), frequent hand washing, avoiding close contact with
sick people, covering coughs and sneezes, avoiding touching face, and staying home when sick.

Treatment: Antiviral medications (oseltamivir, zanamivir, peramivir, baloxavir) most effective within 48 hours of symptom onset.
Supportive care includes rest, fluids, and over-the-counter medications for symptom relief.
"""
    },
    {
        "title": "Tuberculosis (TB)",
        "category": "infectious",
        "content": """
Tuberculosis is a potentially serious infectious disease caused by the bacterium Mycobacterium tuberculosis. It primarily affects
the lungs (pulmonary TB) but can affect other parts of the body (extrapulmonary TB) including kidneys, spine, and brain.

Transmission: Spreads through airborne particles when a person with active pulmonary TB coughs, sneezes, speaks, or sings.
However, TB is not easily transmitted and typically requires prolonged exposure. Not everyone infected develops active disease—
many have latent TB infection (LTBI) where bacteria remain dormant.

Types: Active TB disease (bacteria are active and cause symptoms), latent TB infection (bacteria present but inactive, no symptoms,
not contagious), drug-susceptible TB, multidrug-resistant TB (MDR-TB), and extensively drug-resistant TB (XDR-TB).

Symptoms: Persistent cough lasting more than 3 weeks, coughing up blood or sputum, chest pain, unintentional weight loss,
fatigue, fever, night sweats, chills, and loss of appetite. Extrapulmonary symptoms depend on affected organs.

Risk Factors: HIV infection, immunosuppression, diabetes, kidney disease, malnutrition, tobacco use, alcohol abuse, living in
endemic areas, homelessness, incarceration, and healthcare work.

Diagnosis: Tuberculin skin test (TST), interferon-gamma release assays (IGRAs), chest X-ray, sputum smear microscopy,
culture and drug susceptibility testing, and molecular tests (GeneXpert MTB/RIF).

Treatment: Active TB requires multiple antibiotics for 6-9 months (isoniazid, rifampin, ethambutol, pyrazinamide). Latent TB
treated with shorter regimens. Directly Observed Therapy (DOT) ensures compliance. Drug-resistant TB requires longer treatment
with second-line drugs.
"""
    },
    {
        "title": "HIV/AIDS",
        "category": "infectious",
        "content": """
HIV (Human Immunodeficiency Virus) attacks the body's immune system, specifically CD4 T cells. If untreated, HIV reduces the
number of CD4 cells, making the body vulnerable to opportunistic infections and cancers. AIDS (Acquired Immunodeficiency Syndrome)
is the final stage of HIV infection when the immune system is severely damaged.

Transmission: Unprotected sexual contact, sharing needles or syringes, mother-to-child during pregnancy/birth/breastfeeding,
blood transfusions (rare in countries with screening), and occupational exposure (healthcare workers). HIV is NOT transmitted
through casual contact, saliva, sweat, tears, or closed-mouth kissing.

Stages: Acute HIV infection (2-4 weeks after infection, flu-like symptoms, high viral load), chronic HIV infection (clinical
latency, may last decades with treatment), and AIDS (CD4 count below 200 cells/mm³ or opportunistic infections).

Symptoms: Acute stage: fever, headache, muscle aches, rash, sore throat, swollen lymph nodes. Chronic stage: may have no symptoms
or mild infections. AIDS stage: rapid weight loss, recurring fever, extreme fatigue, prolonged swelling of lymph nodes, diarrhea
lasting more than a week, sores of mouth/anus/genitals, pneumonia, memory loss, depression.

Diagnosis: HIV antibody/antigen tests (4th generation tests detect infection 2-6 weeks after exposure), HIV RNA tests,
CD4 count monitoring, and viral load testing.

Treatment: Antiretroviral therapy (ART) with combination of drugs from different classes: NRTIs, NNRTIs, protease inhibitors,
integrase inhibitors, entry inhibitors. Goals: achieve and maintain undetectable viral load (U=U: undetectable = untransmittable),
preserve immune function, prevent opportunistic infections, and improve quality of life. Pre-exposure prophylaxis (PrEP) and
post-exposure prophylaxis (PEP) for prevention.
"""
    },

    # ==========================================
    # NEUROLOGICAL DISORDERS
    # ==========================================
    {
        "title": "Alzheimer's Disease",
        "category": "neurological",
        "content": """
Alzheimer's disease is a progressive neurodegenerative disorder and the most common cause of dementia, accounting for 60-80%
of cases. It causes brain cells to degenerate and die, leading to continuous decline in memory, thinking, behavior, and social skills.

Pathophysiology: Characterized by accumulation of amyloid-beta plaques and neurofibrillary tangles (tau protein) in the brain,
leading to neuron death and brain tissue loss. Starts in the hippocampus (memory center) and spreads to other brain regions.

Stages: Preclinical (brain changes but no symptoms), mild cognitive impairment (MCI), mild Alzheimer's (early stage),
moderate Alzheimer's (middle stage), and severe Alzheimer's (late stage).

Symptoms: Memory loss affecting daily activities, difficulty planning or solving problems, difficulty completing familiar tasks,
confusion with time or place, trouble understanding visual images and spatial relationships, problems with words in speaking or
writing, misplacing things, decreased judgment, withdrawal from work or social activities, and changes in mood and personality.

Risk Factors: Age (greatest risk factor), family history and genetics (APOE-e4 gene), Down syndrome, mild cognitive impairment,
past head trauma, cardiovascular disease risk factors, low education levels, and lack of cognitive engagement.

Diagnosis: Medical history, cognitive testing (Mini-Mental State Examination, Montreal Cognitive Assessment), neurological exam,
brain imaging (MRI, CT, PET scans), biomarker testing (cerebrospinal fluid analysis), and genetic testing in some cases.

Treatment: No cure exists, but medications can temporarily slow symptom progression. Cholinesterase inhibitors (donepezil,
rivastigmine, galantamine) for mild to moderate stages; memantine for moderate to severe stages. Recently approved monoclonal
antibodies (aducanumab, lecanemab) target amyloid-beta. Non-pharmacological approaches include cognitive stimulation, physical
exercise, social engagement, and structured routines. Caregiver support is essential.
"""
    },
    {
        "title": "Parkinson's Disease",
        "category": "neurological",
        "content": """
Parkinson's disease is a progressive nervous system disorder affecting movement. It develops gradually, sometimes starting with
a barely noticeable tremor in one hand. The disorder results from degeneration of dopamine-producing neurons in the substantia
nigra region of the brain.

Pathophysiology: Loss of dopamine-producing neurons leads to decreased dopamine levels, causing impaired motor control.
Presence of Lewy bodies (abnormal aggregates of alpha-synuclein protein) in brain cells is a hallmark. Exact cause unknown,
likely combination of genetic and environmental factors.

Motor Symptoms: Tremor (often starting in one hand at rest), bradykinesia (slowness of movement), muscle rigidity, postural
instability, freezing of gait, reduced arm swing, shuffling walk, and micrographia (small handwriting).

Non-Motor Symptoms: Depression and anxiety, cognitive changes, sleep disorders, autonomic dysfunction (constipation, urinary
problems, blood pressure changes), loss of smell, fatigue, and pain.

Stages (Hoehn and Yahr Scale): Stage 1 (mild symptoms, one side of body), Stage 2 (symptoms on both sides, no balance impairment),
Stage 3 (balance problems, slowing of movements), Stage 4 (severe symptoms, needs assistance), Stage 5 (wheelchair-bound or bedridden).

Diagnosis: Clinical diagnosis based on medical history and neurological examination. No definitive test, but DaTscan (dopamine
transporter scan) can support diagnosis. MRI to rule out other conditions.

Treatment: Levodopa/Carbidopa (most effective), dopamine agonists (pramipexole, ropinirole), MAO-B inhibitors (selegiline,
rasagiline), COMT inhibitors, anticholinergics, and amantadine. Advanced therapies include deep brain stimulation (DBS),
focused ultrasound, and experimental treatments. Physical therapy, occupational therapy, and speech therapy are important
adjunct treatments.
"""
    },
    {
        "title": "Epilepsy",
        "category": "neurological",
        "content": """
Epilepsy is a neurological disorder characterized by recurrent, unprovoked seizures caused by abnormal electrical activity in
the brain. A seizure is a sudden surge of electrical activity that affects how a person feels or acts.

Types of Seizures: Focal (partial) seizures originate in one area of the brain (simple focal, complex focal). Generalized
seizures involve both sides of the brain from the start (absence, tonic-clonic, myoclonic, atonic, tonic, clonic).

Causes: Genetic factors, head trauma, brain conditions (tumors, strokes), infectious diseases (meningitis, viral encephalitis),
prenatal injury, developmental disorders, and unknown (idiopathic epilepsy).

Symptoms: Vary by seizure type. May include temporary confusion, staring spell, uncontrollable jerking movements, loss of
consciousness, psychic symptoms (fear, déjà vu), muscle stiffness, sudden falls, and autonomic symptoms.

Diagnosis: Detailed medical history, neurological examination, electroencephalogram (EEG) to detect abnormal brain wave patterns,
brain imaging (MRI, CT), neuropsychological tests, and blood tests to rule out other conditions.

Treatment: Anti-epileptic drugs (AEDs) are first-line treatment - includes levetiracetam, valproate, carbamazepine, lamotrigine,
topiramate, and many others. Choice depends on seizure type, age, side effects, and other factors. For drug-resistant epilepsy:
epilepsy surgery (resection, laser ablation), vagus nerve stimulation (VNS), responsive neurostimulation (RNS), ketogenic diet,
and deep brain stimulation. About 70% of people can control seizures with medication.
"""
    },
    {
        "title": "Migraine",
        "category": "neurological",
        "content": """
Migraine is a neurological condition characterized by intense, debilitating headaches often accompanied by nausea, vomiting,
and sensitivity to light and sound. It's one of the most common neurological disorders, affecting about 12% of the population,
with women three times more likely to be affected than men.

Phases: Prodrome (hours to days before, subtle changes like mood changes, neck stiffness, food cravings), aura (visual, sensory,
or motor disturbances lasting 5-60 minutes), attack (4-72 hours of headache pain), and postdrome (after headache, feeling drained
or euphoric).

Types: Migraine without aura (most common), migraine with aura, chronic migraine (15+ headache days per month), hemiplegic migraine,
retinal migraine, and vestibular migraine.

Triggers: Hormonal changes, certain foods (aged cheese, processed meats, alcohol), food additives (MSG, aspartame), caffeine,
stress, sleep changes, intense physical exertion, weather changes, sensory stimuli (bright lights, strong smells), and medications.

Pathophysiology: Involves activation of the trigeminovascular system, cortical spreading depression, release of inflammatory
neuropeptides (CGRP), and changes in brain chemistry including serotonin levels.

Diagnosis: Based on headache history and pattern, neurological examination, and ruling out other causes. International Classification
of Headache Disorders (ICHD) criteria used. Brain imaging if red flags present (sudden severe headache, neurological deficits,
headache after age 50).

Treatment: Acute treatments include NSAIDs, triptans, CGRP antagonists (gepants), ditans, and ergotamines. Preventive treatments
for chronic migraine: beta-blockers, antidepressants, anticonvulsants, CGRP monoclonal antibodies (erenumab, fremanezumab,
galcanezumab), Botox injections, and lifestyle modifications. Non-pharmacological approaches include stress management, regular
sleep schedule, biofeedback, and avoiding triggers.
"""
    },

    # ==========================================
    # GASTROINTESTINAL DISORDERS
    # ==========================================
    {
        "title": "Gastroesophageal Reflux Disease (GERD)",
        "category": "gastrointestinal",
        "content": """
GERD is a chronic digestive disorder where stomach acid or bile flows back into the esophagus, irritating the esophageal lining.
This backflow (reflux) occurs when the lower esophageal sphincter (LES) weakens or relaxes inappropriately.

Mechanism: Normally, the LES acts as a valve that opens to allow food into the stomach and closes to prevent backflow. In GERD,
this mechanism is impaired, allowing acid exposure to the esophagus which lacks protective mucus unlike the stomach.

Symptoms: Heartburn (burning sensation in chest), regurgitation of food or sour liquid, difficulty swallowing (dysphagia),
sensation of a lump in throat, chest pain, chronic cough, laryngitis, new or worsening asthma, and disrupted sleep.

Risk Factors: Obesity, pregnancy, hiatal hernia, connective tissue disorders, delayed stomach emptying, smoking, alcohol use,
large meals, eating late at night, certain foods (fatty/fried foods, chocolate, caffeine, alcohol, acidic foods), and
medications (aspirin, some muscle relaxers, blood pressure medications).

Complications: Esophagitis (inflammation and ulceration), esophageal stricture (narrowing from scar tissue), Barrett's esophagus
(precancerous changes in esophageal lining), and esophageal adenocarcinoma (rare but serious).

Diagnosis: Upper endoscopy, ambulatory acid (pH) probe test, esophageal manometry, and X-ray of upper digestive system.

Treatment: Lifestyle modifications (weight loss, elevate head of bed, avoid trigger foods, smaller meals, don't lie down after
eating, quit smoking). Medications: antacids, H2 blockers (famotidine, ranitidine), proton pump inhibitors (omeprazole,
esomeprazole, lansoprazole), and prokinetic agents. Surgery (Nissen fundoplication) or LINX device for severe cases not
responding to medical therapy.
"""
    },
    {
        "title": "Irritable Bowel Syndrome (IBS)",
        "category": "gastrointestinal",
        "content": """
IBS is a common functional gastrointestinal disorder characterized by abdominal pain and altered bowel habits without structural
abnormalities. It's a disorder of gut-brain interaction affecting 10-15% of the population.

Subtypes: IBS with constipation (IBS-C), IBS with diarrhea (IBS-D), IBS with mixed bowel habits (IBS-M), and IBS unclassified (IBS-U).

Pathophysiology: Complex and multifactorial involving visceral hypersensitivity, altered gut motility, changes in gut microbiome,
low-grade inflammation, immune activation, genetic factors, and psychosocial factors. The gut-brain axis plays a central role.

Symptoms: Abdominal pain or cramping associated with bowel movements, changes in frequency or appearance of bowel movements,
bloating and gas, diarrhea or constipation (or alternating), mucus in stool, and feeling of incomplete evacuation. Symptoms
typically improve after bowel movement.

Triggers: Certain foods (high-FODMAP foods, dairy, gluten in some), stress and anxiety, hormonal changes, infections
(post-infectious IBS), and medications.

Diagnosis: Rome IV criteria require recurrent abdominal pain at least 1 day per week in last 3 months, associated with two or
more: related to defecation, change in stool frequency, change in stool form. Tests to exclude other conditions: blood tests,
stool tests, colonoscopy, and breath tests for SIBO or lactose intolerance.

Treatment: Dietary modifications (low-FODMAP diet, fiber supplementation, avoiding trigger foods), stress management,
psychological therapies (CBT, gut-directed hypnotherapy), medications (antispasmodics, laxatives for IBS-C, loperamide for IBS-D,
rifaximin, eluxadoline, linaclotide, lubiprostone), probiotics, and peppermint oil. Treatment is individualized based on
predominant symptoms.
"""
    },
    {
        "title": "Inflammatory Bowel Disease (IBD)",
        "category": "gastrointestinal",
        "content": """
IBD is a term for chronic inflammatory conditions of the gastrointestinal tract, primarily including Crohn's disease and
ulcerative colitis. These are autoimmune conditions where the immune system attacks the digestive tract.

Crohn's Disease: Can affect any part of GI tract from mouth to anus, most commonly the terminal ileum and colon. Inflammation
is transmural (through all layers of bowel wall), often patchy (skip lesions). Complications include strictures, fistulas,
and abscesses.

Ulcerative Colitis: Limited to colon and rectum, inflammation involves only the innermost lining (mucosa), continuous pattern
starting from rectum and extending proximally. Classified by extent: proctitis, left-sided colitis, pancolitis.

Symptoms: Persistent diarrhea, abdominal pain and cramping, blood in stool, urgency to defecate, weight loss, fatigue, reduced
appetite, and fever. Extraintestinal manifestations: arthritis, skin conditions, eye inflammation, liver disorders.

Pathophysiology: Interaction of genetic susceptibility (over 200 genetic loci identified), environmental factors (smoking, diet,
antibiotics), altered gut microbiome, and immune system dysregulation. Results in chronic inflammation and tissue damage.

Diagnosis: Colonoscopy with biopsies (gold standard), imaging (CT/MRI enterography, capsule endoscopy), blood tests (inflammatory
markers, anemia), stool tests (calprotectin, ruling out infections), and histopathology.

Treatment: Aminosalicylates (5-ASA), corticosteroids for flares, immunomodulators (azathioprine, methotrexate), biologics
(anti-TNF agents, anti-integrin, anti-IL-12/23), JAK inhibitors, antibiotics for complications, and surgery (colectomy for UC,
resection for Crohn's complications). Nutritional therapy, smoking cessation, stress management. Goals: induce and maintain
remission, prevent complications, improve quality of life.
"""
    },

    # ==========================================
    # CANCER
    # ==========================================
    {
        "title": "Lung Cancer",
        "category": "oncology",
        "content": """
Lung cancer is the leading cause of cancer death worldwide. It begins in the lungs and can spread to lymph nodes and other organs.
The vast majority of cases are linked to smoking, though it can occur in never-smokers.

Types: Non-small cell lung cancer (NSCLC, 80-85% of cases) includes adenocarcinoma, squamous cell carcinoma, and large cell
carcinoma. Small cell lung cancer (SCLC, 15-20%) is more aggressive and strongly associated with smoking.

Risk Factors: Smoking (responsible for about 85% of cases), secondhand smoke exposure, radon exposure, asbestos and other
carcinogen exposure, air pollution, family history, previous radiation therapy to chest, and HIV infection.

Symptoms: Persistent cough, coughing up blood, shortness of breath, chest pain, hoarseness, bone pain, headache, weight loss,
and loss of appetite. Many cases are asymptomatic in early stages.

Staging: Uses TNM system (Tumor size, Node involvement, Metastasis). Ranges from stage I (localized) to stage IV (metastatic).
Staging determines treatment approach and prognosis.

Diagnosis: Imaging (chest X-ray, CT scan, PET scan, MRI), sputum cytology, tissue biopsy (bronchoscopy, CT-guided needle biopsy,
thoracoscopy), and molecular testing for mutations (EGFR, ALK, ROS1, PD-L1 expression).

Treatment: Surgery (lobectomy, pneumonectomy) for early-stage disease, radiation therapy (SBRT, conventional), chemotherapy,
targeted therapy (EGFR inhibitors, ALK inhibitors, others based on mutations), immunotherapy (PD-1/PD-L1 inhibitors), and
combination approaches. Treatment plan individualized based on type, stage, molecular profile, and patient factors. Screening
with low-dose CT recommended for high-risk individuals.
"""
    },
    {
        "title": "Breast Cancer",
        "category": "oncology",
        "content": """
Breast cancer is the most common cancer in women worldwide and the second leading cause of cancer death in women. It occurs when
cells in breast tissue grow abnormally and form a tumor. Early detection through screening significantly improves outcomes.

Types: Ductal carcinoma in situ (DCIS, non-invasive), invasive ductal carcinoma (most common, 70-80%), invasive lobular carcinoma,
inflammatory breast cancer (rare, aggressive), triple-negative breast cancer, HER2-positive breast cancer, and hormone
receptor-positive cancers.

Risk Factors: Female gender, increasing age, genetic mutations (BRCA1, BRCA2, others), family history, personal history of breast
conditions, radiation exposure, obesity, alcohol consumption, hormone therapy, never having been pregnant, and first pregnancy
after age 30.

Symptoms: Lump or mass in breast or underarm, change in size or shape, skin dimpling or puckering, nipple changes (inversion,
discharge), redness or scaling of nipple or breast skin, and pain (though most breast cancers are painless).

Diagnosis: Mammography (screening and diagnostic), ultrasound, MRI, biopsy (fine needle aspiration, core needle, surgical),
and biomarker testing (ER, PR, HER2 status, genetic testing).

Staging: Stage 0 (DCIS) to Stage IV (metastatic). Considers tumor size, lymph node involvement, metastasis, grade, and biomarker status.

Treatment: Surgery (lumpectomy, mastectomy), sentinel lymph node biopsy or axillary dissection, radiation therapy, chemotherapy
(neoadjuvant or adjuvant), hormone therapy (tamoxifen, aromatase inhibitors for ER/PR+ cancers), HER2-targeted therapy (trastuzumab,
pertuzumab for HER2+ cancers), CDK4/6 inhibitors, and immunotherapy for triple-negative. Reconstruction options available.
Screening guidelines: mammography starting at age 40-50, clinical breast exams, breast self-awareness. Genetic counseling for
high-risk individuals.
"""
    },
    {
        "title": "Colorectal Cancer",
        "category": "oncology",
        "content": """
Colorectal cancer is cancer that begins in the colon or rectum. Most colorectal cancers develop from polyps (abnormal growths)
over 10-15 years, making screening crucial for prevention through polyp detection and removal.

Pathophysiology: Develops through adenoma-carcinoma sequence. Genetic mutations accumulate (APC, KRAS, TP53), leading to
transformation from normal mucosa to adenoma to carcinoma. Can be sporadic (95%) or hereditary (5% - Lynch syndrome, FAP).

Risk Factors: Age over 50, personal or family history of colorectal cancer or polyps, inflammatory bowel disease, inherited
syndromes (Lynch syndrome, FAP), type 2 diabetes, obesity, physical inactivity, high-fat/low-fiber diet, red and processed
meat consumption, smoking, and heavy alcohol use.

Symptoms: Change in bowel habits (diarrhea, constipation), rectal bleeding or blood in stool, abdominal discomfort (cramps,
gas, pain), feeling of incomplete evacuation, weakness and fatigue, unintended weight loss. Early stages often asymptomatic.

Diagnosis: Colonoscopy with biopsy (gold standard for diagnosis and screening), fecal occult blood testing, CT colonography,
flexible sigmoidoscopy, CEA blood test, imaging for staging (CT, MRI, PET), and molecular testing (KRAS, NRAS, BRAF, MSI status).

Staging: Stage I (localized to bowel wall) to Stage IV (distant metastases, commonly liver and lungs). TNM classification used.

Treatment: Surgery (polypectomy, colectomy, proctectomy with or without ostomy) is primary treatment for localized disease.
Chemotherapy (FOLFOX, FOLFIRI regimens), targeted therapy (bevacizumab, cetuximab, panitumumab for specific mutations),
immunotherapy (pembrolizumab, nivolumab for MSI-high tumors), and radiation (mainly for rectal cancer). Treatment approach
depends on location, stage, and molecular profile. Screening recommendations: begin at age 45-50 with colonoscopy every 10 years
or other approved screening methods.
"""
    },

    # ==========================================
    # MENTAL HEALTH DISORDERS
    # ==========================================
    {
        "title": "Major Depressive Disorder",
        "category": "mental_health",
        "content": """
Major Depressive Disorder (MDD) is a common and serious medical illness characterized by persistent feelings of sadness,
hopelessness, and loss of interest in activities. It affects how a person feels, thinks, and behaves, and can lead to various
emotional and physical problems.

Pathophysiology: Involves complex interactions of neurotransmitter systems (serotonin, norepinephrine, dopamine), genetic
factors, structural and functional brain changes, HPA axis dysregulation, inflammation, and neuroplasticity alterations.

Diagnostic Criteria (DSM-5): At least 5 symptoms present for 2 weeks, including either depressed mood or loss of interest/pleasure,
plus symptoms like weight/appetite changes, sleep disturbance, psychomotor agitation or retardation, fatigue, feelings of
worthlessness/guilt, concentration difficulties, or recurrent thoughts of death/suicide.

Symptoms: Persistent sad or empty mood, loss of interest in hobbies, changes in appetite/weight, sleep disturbances (insomnia
or hypersomnia), fatigue, psychomotor changes, feelings of worthlessness or excessive guilt, difficulty concentrating or making
decisions, recurrent thoughts of death or suicide, and physical symptoms (headaches, digestive problems).

Types: Single episode vs recurrent, with anxious distress, with melancholic features, with atypical features, with psychotic
features, with seasonal pattern (seasonal affective disorder), peripartum onset, and persistent depressive disorder (dysthymia).

Risk Factors: Family history, previous depressive episodes, major life changes/stress, trauma/abuse, chronic medical conditions,
substance abuse, certain medications, and other mental health disorders.

Diagnosis: Clinical interview, symptom assessment (PHQ-9, Beck Depression Inventory), medical history, physical exam, and lab
tests to rule out other conditions (thyroid problems, vitamin deficiencies).

Treatment: Psychotherapy (cognitive behavioral therapy, interpersonal therapy, psychodynamic therapy), antidepressant medications
(SSRIs, SNRIs, TCAs, MAOIs, atypical antidepressants), combination therapy, ECT for severe/treatment-resistant cases, TMS,
ketamine/esketamine for treatment-resistant depression, and lifestyle modifications (exercise, sleep hygiene, social support,
stress management). Treatment typically lasts 6-12 months minimum to prevent relapse.
"""
    },
    {
        "title": "Generalized Anxiety Disorder",
        "category": "mental_health",
        "content": """
Generalized Anxiety Disorder (GAD) is characterized by persistent and excessive worry about various aspects of daily life.
The worry is difficult to control and is accompanied by physical symptoms. It interferes with daily functioning and relationships.

Diagnostic Criteria: Excessive anxiety and worry occurring more days than not for at least 6 months, about various events or
activities. Difficulty controlling worry. Associated with three or more symptoms: restlessness, easily fatigued, difficulty
concentrating, irritability, muscle tension, sleep disturbance.

Pathophysiology: Involves dysregulation of fear circuitry in the brain (amygdala hyperactivity, prefrontal cortex hypofunction),
neurotransmitter imbalances (GABA, serotonin, norepinephrine), genetic factors (30-40% heritability), and environmental stressors.

Symptoms: Excessive worry about everyday matters, difficulty controlling worrisome thoughts, knowing worry is excessive but
can't stop, restlessness or feeling on edge, fatigue, difficulty concentrating or mind going blank, irritability, muscle tension
and aches, trembling or twitching, sleep problems, sweating, nausea, diarrhea, and exaggerated startle response.

Physical Manifestations: Headaches, stomach problems, muscle tension, difficulty swallowing, trembling, twitching, irritability,
sweating, nausea, lightheadedness, frequent urination, and shortness of breath.

Risk Factors: Family history, personality factors (tendency toward negative thinking, behavioral inhibition), trauma or stressful
life events, chronic medical conditions, substance abuse, and other mental health disorders.

Diagnosis: Clinical interview, anxiety rating scales (GAD-7), medical evaluation to rule out physical causes (thyroid problems,
caffeine/medication effects, heart conditions), and assessment for comorbid conditions.

Treatment: Cognitive Behavioral Therapy (CBT) - first-line treatment, particularly effective. Medications: SSRIs and SNRIs
(first-line - escitalopram, sertraline, venlafaxine, duloxetine), buspirone, benzodiazepines (short-term only due to dependence
risk), and pregabalin. Relaxation techniques, mindfulness meditation, exercise, sleep hygiene, limiting caffeine/alcohol, and
stress management. Combination of therapy and medication often most effective.
"""
    },
    {
        "title": "Bipolar Disorder",
        "category": "mental_health",
        "content": """
Bipolar disorder is a mental health condition characterized by extreme mood swings including emotional highs (mania or hypomania)
and lows (depression). These mood shifts affect energy, activity levels, judgment, behavior, and the ability to function.

Types: Bipolar I (manic episodes lasting at least 7 days or severe enough to need hospitalization, usually depressive episodes
occur as well), Bipolar II (pattern of depressive and hypomanic episodes but not full manic episodes), and Cyclothymic Disorder
(periods of hypomanic and depressive symptoms for at least 2 years but don't meet criteria for hypomanic or depressive episodes).

Manic Episode Symptoms: Abnormally elevated or irritable mood, increased energy/activity, decreased need for sleep, racing thoughts,
rapid speech, grandiosity, poor judgment, risky behaviors (excessive spending, sexual indiscretions, impulsive decisions),
distractibility, and sometimes psychotic features.

Hypomanic Episode: Similar to mania but less severe, doesn't cause major impairment in functioning, no psychotic features,
lasts at least 4 consecutive days.

Depressive Episode: Identical to major depressive disorder - persistent sadness, loss of interest, changes in sleep/appetite,
fatigue, feelings of worthlessness, difficulty concentrating, suicidal thoughts.

Risk Factors: Strong genetic component (first-degree relatives have 10-fold increased risk), brain structure and chemistry
differences, periods of high stress, drug or alcohol abuse, and sometimes triggered by major life changes.

Diagnosis: Psychiatric evaluation, mood charting, assessment of mood episode patterns, medical evaluation to rule out other
conditions, and sometimes rating scales (Young Mania Rating Scale, Mood Disorder Questionnaire).

Treatment: Mood stabilizers (lithium - gold standard, valproate, carbamazepine, lamotrigine), atypical antipsychotics (quetiapine,
olanzapine, aripiprazole, lurasidone), antidepressants (used cautiously with mood stabilizer to prevent mania), psychotherapy
(CBT, family-focused therapy, interpersonal and social rhythm therapy), psychoeducation, sleep regulation, substance abuse
treatment if needed, and ECT for severe cases. Lifelong treatment necessary; stopping medication leads to relapse in most cases.
"""
    },

    # ==========================================
    # AUTOIMMUNE DISORDERS
    # ==========================================
    {
        "title": "Rheumatoid Arthritis",
        "category": "autoimmune",
        "content": """
Rheumatoid Arthritis (RA) is a chronic autoimmune disease causing inflammation of the joints and surrounding tissues. Unlike
osteoarthritis (wear-and-tear), RA involves the immune system attacking the synovium (joint lining), potentially affecting
other organs as well.

Pathophysiology: Immune system mistakenly attacks synovial membrane, causing inflammation. This leads to synovial thickening,
cartilage and bone erosion, and joint deformity. Autoantibodies (rheumatoid factor, anti-CCP) contribute to disease process.
Inflammatory cytokines (TNF-alpha, IL-6) play central roles.

Symptoms: Joint pain, swelling, and stiffness (especially morning stiffness lasting >30 minutes), symmetrical joint involvement,
fatigue, fever, loss of appetite, rheumatoid nodules, and reduced range of motion. Commonly affects hands, wrists, knees, and feet.

Extra-articular Manifestations: Rheumatoid nodules, pulmonary involvement (interstitial lung disease, pleural effusion),
cardiovascular disease (increased risk), eye problems (scleritis, episcleritis), vasculitis, and Felty's syndrome.

Diagnosis: Clinical evaluation, blood tests (RF, anti-CCP antibodies, ESR, CRP), imaging (X-rays, ultrasound, MRI), and
synovial fluid analysis. ACR/EULAR classification criteria used.

Treatment: Disease-modifying antirheumatic drugs (DMARDs) started early - conventional DMARDs (methotrexate is first-line,
sulfasalazine, hydroxychloroquine, leflunomide), biologic DMARDs (TNF inhibitors, IL-6 inhibitors, B-cell depletion, T-cell
costimulation inhibitors), JAK inhibitors (tofacitinib, baricitinib), NSAIDs for symptom relief, corticosteroids for acute
flares, physical/occupational therapy, and surgery for severe joint damage. Early aggressive treatment prevents joint damage.
Treat-to-target approach aims for remission or low disease activity.
"""
    },
    {
        "title": "Systemic Lupus Erythematosus (SLE)",
        "category": "autoimmune",
        "content": """
Systemic Lupus Erythematosus is a chronic autoimmune disease where the immune system attacks healthy tissues throughout the body,
affecting skin, joints, kidneys, brain, heart, lungs, and blood cells. It's characterized by periods of flares and remissions.

Pathophysiology: Loss of self-tolerance leads to production of autoantibodies (anti-dsDNA, anti-Smith, antiphospholipid),
immune complex formation and deposition, complement activation, and multi-organ inflammation and damage. Genetic, hormonal,
and environmental factors contribute.

Symptoms: Highly variable. Malar (butterfly) rash across cheeks and nose, discoid rash, photosensitivity, oral/nasal ulcers,
arthritis (typically non-erosive), serositis (pleuritis, pericarditis), renal involvement (lupus nephritis), neuropsychiatric
manifestations (seizures, psychosis), hematologic abnormalities (anemia, leukopenia, thrombocytopenia), and constitutional
symptoms (fatigue, fever, weight loss).

Organ System Involvement: Kidneys (lupus nephritis - major cause of morbidity), cardiovascular (accelerated atherosclerosis,
myocarditis), pulmonary (pleuritis, pneumonitis), neuropsychiatric (headaches, cognitive dysfunction, psychosis), hematologic
(autoimmune hemolytic anemia, thrombocytopenia), and skin/mucous membranes.

Diagnosis: ACR/EULAR classification criteria, ANA testing (positive in >95%), specific autoantibody testing (anti-dsDNA,
anti-Smith, antiphospholipid), complement levels (C3, C4 - often low during active disease), complete blood count, urinalysis,
renal biopsy if nephritis suspected, and imaging as needed.

Treatment: Depends on severity and organs involved. Hydroxychloroquine (antimalarial - foundation of treatment for all patients),
NSAIDs, corticosteroids (varying doses based on severity), immunosuppressants (azathioprine, mycophenolate mofetil,
cyclophosphamide for severe disease), biologics (belimumab, rituximab), sun protection, monitoring for complications,
management of comorbidities (hypertension, hyperlipidemia), and lifestyle modifications. Pregnancy requires special management.
Regular monitoring for organ damage essential.
"""
    },
    {
        "title": "Multiple Sclerosis",
        "category": "autoimmune",
        "content": """
Multiple Sclerosis is a chronic autoimmune disease of the central nervous system where the immune system attacks the myelin
sheath protecting nerve fibers, disrupting communication between the brain and body. The damage can affect brain, spinal cord,
and optic nerves.

Types: Relapsing-Remitting MS (RRMS - 85% of cases, distinct relapses with recovery), Secondary Progressive MS (SPMS - follows
RRMS, gradual worsening), Primary Progressive MS (PPMS - gradual onset and worsening without distinct relapses), and
Progressive-Relapsing MS (rare).

Pathophysiology: Autoimmune attack on myelin and oligodendrocytes leads to demyelination, inflammation, axonal damage, and
sclerotic plaques (lesions) in CNS. Blood-brain barrier breakdown allows immune cells to enter CNS. Both inflammatory and
neurodegenerative processes occur.

Symptoms: Highly variable depending on lesion location. Fatigue, numbness/tingling, weakness, vision problems (optic neuritis,
diplopia), balance and coordination problems, bladder/bowel dysfunction, cognitive changes, depression, pain, spasticity,
and vertigo. Heat sensitivity (Uhthoff's phenomenon) is common.

Diagnosis: McDonald criteria used. Brain and spinal cord MRI showing characteristic lesions (dissemination in space and time),
lumbar puncture showing oligoclonal bands in CSF, evoked potential tests, and clinical history of attacks. Must rule out
other conditions.

Treatment: Disease-modifying therapies (DMTs) reduce relapses and slow progression - injectable medications (interferons,
glatiramer acetate), oral medications (fingolimod, teriflunomide, dimethyl fumarate, cladribine), infusion therapies (natalizumab,
ocrelizumab, alemtuzumab). High-dose corticosteroids for acute relapses. Symptomatic treatments for spasticity, pain, fatigue,
bladder problems. Physical therapy, occupational therapy, cognitive rehabilitation. Early treatment important to prevent disability
accumulation. Regular MRI monitoring.
"""
    },

    # ==========================================
    # RENAL DISORDERS
    # ==========================================
    {
        "title": "Chronic Kidney Disease",
        "category": "renal",
        "content": """
Chronic Kidney Disease (CKD) is the gradual loss of kidney function over time. The kidneys filter wastes and excess fluids from
blood, which are then excreted in urine. CKD can progress to end-stage renal disease (kidney failure) requiring dialysis or
transplantation.

Stages: Based on GFR (glomerular filtration rate). Stage 1 (GFR ≥90, kidney damage with normal function), Stage 2 (GFR 60-89,
mild reduction), Stage 3a (GFR 45-59, mild-moderate reduction), Stage 3b (GFR 30-44, moderate-severe reduction), Stage 4
(GFR 15-29, severe reduction), Stage 5 (GFR <15, kidney failure).

Causes: Diabetes (leading cause - diabetic nephropathy), hypertension, glomerulonephritis, polycystic kidney disease, prolonged
obstruction, recurrent kidney infections, vesicoureteral reflux, and medications (NSAIDs, some antibiotics).

Symptoms: Early stages often asymptomatic. As disease progresses: fatigue, swelling in feet and ankles, decreased urine output,
shortness of breath, nausea, loss of appetite, sleep problems, decreased mental sharpness, muscle cramps, hypertension, and
uremia (buildup of toxins).

Complications: Fluid retention, hyperkalemia (high potassium), cardiovascular disease, anemia, bone disease (renal osteodystrophy),
metabolic acidosis, malnutrition, and complications affecting central nervous system.

Diagnosis: Blood tests (serum creatinine, BUN, GFR calculation), urine tests (albumin, protein, sediment examination), imaging
(ultrasound, CT), and sometimes kidney biopsy.

Treatment: Underlying cause management (blood sugar control for diabetes, blood pressure control), medications (ACE inhibitors
or ARBs to slow progression, diuretics, phosphate binders, erythropoietin-stimulating agents for anemia, vitamin D), dietary
modifications (protein restriction, potassium/phosphorus/sodium restriction), fluid management, and preparation for renal
replacement therapy (hemodialysis, peritoneal dialysis, kidney transplantation) when reaching Stage 5. Regular monitoring
of kidney function, complications, and comorbidities essential.
"""
    },
    {
        "title": "Acute Kidney Injury",
        "category": "renal",
        "content": """
Acute Kidney Injury (AKI), formerly called acute renal failure, is a sudden episode of kidney failure or kidney damage that
happens within a few hours or days. It causes waste products to build up in blood and makes it hard for kidneys to maintain
correct fluid balance.

Classification: Prerenal (reduced blood flow to kidneys - 70% of cases), intrarenal/intrinsic (direct damage to kidney tissue -
25% of cases), and postrenal (obstruction of urinary tract - 5% of cases).

Causes: Prerenal: dehydration, hemorrhage, heart failure, sepsis, liver cirrhosis, medications (NSAIDs, ACE inhibitors).
Intrarenal: acute tubular necrosis (ATN - most common), glomerulonephritis, interstitial nephritis, vascular obstruction.
Postrenal: kidney stones, tumors, enlarged prostate, neurogenic bladder.

RIFLE/AKIN/KDIGO Criteria: Diagnosis based on increase in serum creatinine and/or decrease in urine output. KDIGO stages
based on creatinine rise and urine output: Stage 1 (1.5-1.9x baseline or ≥0.3 mg/dL increase), Stage 2 (2.0-2.9x baseline),
Stage 3 (3.0x baseline or ≥4.0 mg/dL or initiation of RRT).

Symptoms: Decreased urine output (oliguria or anuria), fluid retention causing swelling, shortness of breath, fatigue, confusion,
nausea, seizures or coma in severe cases, chest pain or pressure. Some cases are asymptomatic and detected only through lab tests.

Diagnosis: Serum creatinine and BUN measurement, urine output monitoring, urinalysis, urine electrolytes and osmolality,
imaging (ultrasound to rule out obstruction), and sometimes kidney biopsy if etiology unclear.

Treatment: Identify and treat underlying cause, discontinue nephrotoxic medications, fluid and electrolyte management,
nutritional support, medication dose adjustments, avoid contrast agents, treat complications (hyperkalemia, metabolic acidosis,
fluid overload), and dialysis if severe (indications: refractory hyperkalemia, severe acidosis, uremia, fluid overload).
Many cases are reversible with prompt treatment. Prevention important in hospitalized patients through adequate hydration,
avoiding nephrotoxins, and careful medication management.
"""
    },

    # ==========================================
    # DERMATOLOGY
    # ==========================================
    {
        "title": "Psoriasis",
        "category": "dermatology",
        "content": """
Psoriasis is a chronic autoimmune skin condition that causes rapid buildup of skin cells, resulting in scaling on the skin's
surface. Inflammation and redness around the scales are common. Psoriatic scales are whitish-silver and develop in thick,
red patches that sometimes crack and bleed.

Pathophysiology: T-cell mediated autoimmune process with overactive immune response causing accelerated skin cell production
cycle (days instead of weeks). Involves cytokines IL-17, IL-23, TNF-alpha. Genetic and environmental factors contribute.

Types: Plaque psoriasis (most common - 80-90%), guttate psoriasis (small drop-shaped lesions), inverse psoriasis (smooth red
patches in skin folds), pustular psoriasis (white pustules surrounded by red skin), and erythrodermic psoriasis (rare, severe,
widespread redness and shedding).

Symptoms: Red patches of skin covered with thick silvery scales, dry cracked skin that may bleed, itching/burning/soreness,
thickened pitted or ridged nails, and swollen stiff joints (psoriatic arthritis in 30% of patients).

Triggers: Infections (especially strep throat), skin injury (Koebner phenomenon), stress, smoking, heavy alcohol consumption,
vitamin D deficiency, certain medications (beta-blockers, lithium, antimalarials), and cold weather.

Complications: Psoriatic arthritis, eye conditions, obesity, type 2 diabetes, hypertension, cardiovascular disease, other
autoimmune diseases, kidney disease, and mental health conditions (depression, anxiety).

Diagnosis: Clinical examination, skin biopsy if diagnosis uncertain, assessment of severity using PASI (Psoriasis Area and
Severity Index) or BSA (Body Surface Area).

Treatment: Topical (first-line for mild-moderate): corticosteroids, vitamin D analogues, retinoids, calcineurin inhibitors,
salicylic acid, coal tar. Phototherapy: UVB, PUVA. Systemic (moderate-severe): methotrexate, cyclosporine, acitretin.
Biologics: TNF-alpha inhibitors (adalimumab, etanercept), IL-12/23 inhibitor (ustekinumab), IL-17 inhibitors (secukinumab,
ixekizumab), IL-23 inhibitors (guselkumab, risankizumab). Small molecules: apremilast, deucravacitinib. Treatment selection
based on severity, location, impact on quality of life, and comorbidities.
"""
    },
    {
        "title": "Eczema (Atopic Dermatitis)",
        "category": "dermatology",
        "content": """
Atopic dermatitis, commonly called eczema, is a chronic inflammatory skin condition causing itchy, red, swollen, and cracked
skin. It often appears in childhood but can occur at any age. It's part of the "atopic triad" along with asthma and allergic rhinitis.

Pathophysiology: Skin barrier dysfunction (reduced filaggrin protein), immune dysregulation (Th2-skewed response), genetic
factors, environmental triggers, and altered skin microbiome. The impaired barrier allows allergen penetration and water loss.

Symptoms: Intense itching (especially at night), red to brownish-gray patches, small raised bumps that may leak fluid when
scratched, crusty patches from dried leaked fluid, thickened cracked scaly skin (lichenification), raw sensitive swollen skin
from scratching, and areas commonly affected include hands, feet, ankles, wrists, neck, upper chest, eyelids, inside elbows
and knees, face and scalp (especially in infants).

Triggers: Dry skin, irritants (soaps, detergents, disinfectants), allergens (dust mites, pet dander, pollen), microbes
(bacteria, viruses, fungi), heat and sweating, stress, and certain foods in some individuals.

Complications: Asthma and hay fever, chronic itchy scaly skin, skin infections (staph or herpes), irritant hand dermatitis,
allergic contact dermatitis, and sleep problems.

Diagnosis: Clinical examination, personal and family history, patch testing if allergic contact dermatitis suspected, and
sometimes skin biopsy to rule out other conditions.

Treatment: Skin care and moisturization (emollients multiple times daily - cornerstone of therapy), topical corticosteroids
(various potencies based on severity and location), topical calcineurin inhibitors (tacrolimus, pimecrolimus), PDE4 inhibitor
(crisaborole), barrier repair creams, wet wrap therapy for severe cases, phototherapy, systemic immunosuppressants for severe
cases (cyclosporine, methotrexate, azathioprine), biologics (dupilumab - IL-4/IL-13 inhibitor), JAK inhibitors (baricitinib,
upadacitinib, abrocitinib), antihistamines for itch, treating infections promptly, identifying and avoiding triggers, stress
management, and maintaining proper skin hygiene. Avoid scratching (itch-scratch cycle worsens condition).
"""
    },

    # ==========================================
    # HEMATOLOGY
    # ==========================================
    {
        "title": "Anemia",
        "category": "hematology",
        "content": """
Anemia is a condition where you lack enough healthy red blood cells to carry adequate oxygen to body tissues. This can make
you feel tired and weak. There are many forms of anemia, each with different causes.

Types and Causes: Iron deficiency anemia (most common - inadequate iron intake, blood loss, pregnancy, poor absorption),
vitamin deficiency anemia (B12, folate), anemia of chronic disease (cancer, HIV/AIDS, rheumatoid arthritis), aplastic anemia
(bone marrow failure), hemolytic anemias (premature RBC destruction), sickle cell anemia (genetic), thalassemia (genetic),
and anemia caused by bone marrow diseases.

Pathophysiology: Decreased RBC production (nutritional deficiencies, bone marrow problems, chronic diseases), increased RBC
destruction (hemolysis), or blood loss (acute or chronic bleeding).

Symptoms: Fatigue, weakness, pale or yellowish skin, irregular heartbeat, shortness of breath, dizziness or lightheadedness,
chest pain, cold hands and feet, headache, and in severe cases, pica (craving for non-food items like ice, dirt).

Complications: Severe fatigue affecting quality of life, pregnancy complications, heart problems (arrhythmias, heart failure
from increased workload), growth delays in children, and in severe cases, life-threatening complications.

Diagnosis: Complete blood count (CBC) measuring hemoglobin, hematocrit, MCV (mean corpuscular volume), peripheral blood smear,
reticulocyte count, iron studies (serum iron, ferritin, transferrin, TIBC), vitamin B12 and folate levels, hemoglobin
electrophoresis, bone marrow biopsy in select cases, and tests to identify bleeding source if indicated.

Classification by MCV: Microcytic (low MCV - iron deficiency, thalassemia), normocytic (normal MCV - blood loss, chronic
disease, hemolysis), macrocytic (high MCV - B12/folate deficiency, alcohol use, certain medications).

Treatment: Depends on cause. Iron deficiency: oral or IV iron supplementation, treat underlying bleeding. B12 deficiency:
B12 injections or high-dose oral supplementation. Folate deficiency: folic acid supplements. Chronic disease: treat underlying
condition, erythropoietin-stimulating agents. Hemolytic anemia: immunosuppression, splenectomy, treat underlying cause.
Aplastic anemia: immunosuppression, bone marrow transplant. Blood transfusions for severe symptomatic anemia.
"""
    },
    {
        "title": "Sickle Cell Disease",
        "category": "hematology",
        "content": """
Sickle cell disease is an inherited red blood cell disorder where hemoglobin is abnormal, causing RBCs to become rigid and
shaped like sickles or crescent moons. These cells die early and can block blood flow, causing pain and organ damage.

Genetics: Autosomal recessive disorder caused by mutation in beta-globin gene (HBB). Homozygous (HbSS) causes sickle cell anemia
(most severe form). Heterozygous (HbAS) is sickle cell trait (usually asymptomatic, carrier state). Compound heterozygous forms
include HbSC, HbS-beta thalassemia.

Pathophysiology: Abnormal hemoglobin S polymerizes when deoxygenated, distorting RBC shape. Sickled cells are rigid, causing
vaso-occlusion (blocking small blood vessels), hemolysis (premature RBC destruction), and chronic inflammation. Results in
tissue ischemia, pain, and organ damage.

Acute Complications: Vaso-occlusive crisis (severe pain episodes), acute chest syndrome (life-threatening - chest pain, fever,
infiltrates on X-ray), splenic sequestration (blood trapped in spleen), aplastic crisis (usually triggered by parvovirus B19),
stroke, and priapism.

Chronic Complications: Chronic pain, avascular necrosis (especially hip and shoulder), pulmonary hypertension, chronic kidney
disease, retinopathy, delayed growth and puberty, leg ulcers, and increased infection risk (especially encapsulated organisms
due to functional asplenia).

Diagnosis: Newborn screening (hemoglobin electrophoresis or HPLC), complete blood count showing anemia, peripheral smear showing
sickled cells, reticulocytosis, and prenatal genetic testing available.

Treatment: Hydroxyurea (increases fetal hemoglobin, reduces crises), L-glutamine, crizanlizumab (prevents vaso-occlusion),
voxelotor (reduces sickling), chronic transfusion therapy, pain management for crises, prophylactic antibiotics (penicillin in
childhood), comprehensive vaccinations, folic acid supplementation, management of complications, and hematopoietic stem cell
transplantation (only curative option). Gene therapy emerging as potential cure. Supportive care includes adequate hydration,
avoiding triggers (dehydration, extreme temperatures, high altitudes, stress), and regular healthcare monitoring.
"""
    },

    # ==========================================
    # IMMUNOLOGY & ALLERGIES
    # ==========================================
    {
        "title": "The Immune System",
        "category": "immunology",
        "content": """
The immune system is a complex network of cells, tissues, and organs that work together to defend the body against harmful
pathogens (bacteria, viruses, parasites, fungi) and abnormal cells. It distinguishes self from non-self and remembers previous
encounters with pathogens.

Components: Innate immunity (immediate, non-specific defense - physical barriers, phagocytes, NK cells, complement system) and
adaptive immunity (delayed, specific defense with memory - T cells, B cells, antibodies).

Cells: White blood cells (leukocytes) including neutrophils (most abundant, first responders), lymphocytes (T cells, B cells,
NK cells), monocytes/macrophages (phagocytosis, antigen presentation), dendritic cells (antigen presentation), eosinophils
(parasites, allergies), and basophils/mast cells (allergic responses).

Organs: Primary lymphoid organs (bone marrow where all immune cells originate, thymus where T cells mature) and secondary
lymphoid organs (lymph nodes, spleen, tonsils, Peyer's patches, appendix - where immune responses are mounted).

Innate Immune Response: Physical barriers (skin, mucous membranes), chemical barriers (stomach acid, antimicrobial peptides),
cellular defenses (phagocytes, NK cells), complement system (cascade of proteins that tag pathogens and create membrane attack
complex), and inflammatory response.

Adaptive Immune Response: Cell-mediated immunity (T cells - CD8+ cytotoxic T cells kill infected cells, CD4+ helper T cells
coordinate immune response, regulatory T cells prevent autoimmunity) and humoral immunity (B cells produce antibodies -
IgM, IgG, IgA, IgE, IgD).

Memory: After first exposure to pathogen, memory B and T cells remain, allowing faster, stronger response upon re-exposure.
This is basis for vaccination and long-term immunity.

Immunological Disorders: Immunodeficiency (primary like SCID, or secondary like HIV/AIDS), autoimmunity (immune system attacks
self - lupus, rheumatoid arthritis, type 1 diabetes), hypersensitivity (allergies, asthma), and chronic inflammation.
"""
    },
    {
        "title": "Allergic Rhinitis (Hay Fever)",
        "category": "immunology",
        "content": """
Allergic rhinitis is an allergic response causing inflammation of the nasal mucosa. When exposed to allergens, the immune system
overreacts, triggering symptoms. It can be seasonal (pollen, mold spores) or perennial (dust mites, pet dander, cockroaches).

Pathophysiology: Type I hypersensitivity reaction. Initial sensitization produces allergen-specific IgE antibodies that bind
to mast cells. Re-exposure causes cross-linking of IgE, triggering mast cell degranulation and release of histamine and other
mediators, causing acute symptoms. Late-phase reaction involves influx of inflammatory cells.

Symptoms: Sneezing, runny nose (rhinorrhea), nasal congestion, itchy nose/eyes/throat, postnasal drip, cough, fatigue, decreased
sense of smell, and allergic shiners (dark circles under eyes from nasal congestion).

Triggers: Seasonal allergens (tree pollen in spring, grass pollen in late spring/summer, ragweed pollen in fall, mold spores)
and perennial allergens (dust mites, pet dander, cockroach droppings, indoor mold).

Complications: Reduced quality of life, sleep disturbances, impaired concentration and productivity, sinusitis, ear infections
(especially in children), and worsening of asthma if present.

Diagnosis: Clinical history, physical examination, allergy testing (skin prick test or specific IgE blood test), and sometimes
nasal endoscopy.

Treatment: Allergen avoidance (primary strategy), pharmacotherapy (intranasal corticosteroids - first-line treatment, oral
antihistamines, intranasal antihistamines, leukotriene receptor antagonists, decongestants for short-term use, intranasal
cromolyn), immunotherapy (allergy shots or sublingual tablets - modifies immune response, effective for long-term control),
nasal saline irrigation, and managing comorbidities. Intranasal corticosteroids most effective for moderate-severe symptoms.
Environmental control measures include using allergen-proof bedding covers, HEPA filters, maintaining low humidity, regular
cleaning, and keeping windows closed during high pollen seasons.
"""
    },

    # ==========================================
    # OPHTHALMOLOGY
    # ==========================================
    {
        "title": "Glaucoma",
        "category": "ophthalmology",
        "content": """
Glaucoma is a group of eye conditions that damage the optic nerve, often due to elevated intraocular pressure (IOP). It's a
leading cause of irreversible blindness. Damage occurs gradually and vision loss is permanent, making early detection crucial.

Types: Primary open-angle glaucoma (most common, gradual onset), angle-closure glaucoma (acute or chronic, medical emergency
if acute), normal-tension glaucoma (optic nerve damage despite normal IOP), congenital glaucoma, and secondary glaucoma
(due to other conditions - diabetes, eye trauma, medications, tumors).

Pathophysiology: Impaired drainage of aqueous humor through trabecular meshwork leads to increased IOP in most cases. Elevated
pressure damages retinal ganglion cells and optic nerve fibers. In normal-tension glaucoma, vascular insufficiency may play
a role.

Risk Factors: Elevated IOP, age over 60, family history, African, Hispanic, or Asian ancestry, thin corneas, extreme nearsightedness
or farsightedness, eye injury, prolonged corticosteroid use, and certain medical conditions (diabetes, high blood pressure,
heart disease).

Symptoms: Primary open-angle glaucoma - often no symptoms until significant vision loss (peripheral vision loss first, tunnel
vision in advanced stages). Acute angle-closure glaucoma - severe eye pain, headache, nausea/vomiting, blurred vision, halos
around lights, red eye, sudden vision loss (medical emergency).

Diagnosis: Comprehensive eye exam including tonometry (IOP measurement), ophthalmoscopy (optic nerve examination), visual field
test (perimetry), gonioscopy (drainage angle examination), pachymetry (corneal thickness), and optical coherence tomography
(OCT - optic nerve fiber layer analysis).

Treatment: Goal is to lower IOP to prevent further damage. Medications: prostaglandin analogs (latanoprost - first-line),
beta-blockers (timolol), alpha-adrenergic agonists (brimonidine), carbonic anhydrase inhibitors (dorzolamide), and
cholinergic agents (pilocarpine). Laser procedures: trabeculoplasty, iridotomy. Surgery: trabeculectomy, drainage implants,
minimally invasive glaucoma surgery (MIGS). Treatment is lifelong. Regular monitoring essential. Once vision is lost, it cannot
be restored.
"""
    },

    # ==========================================
    # NUTRITION & METABOLISM
    # ==========================================
    {
        "title": "Obesity",
        "category": "nutrition",
        "content": """
Obesity is a complex disease involving excessive body fat that increases the risk of health problems. It's defined by body mass
index (BMI): overweight is 25-29.9, obesity is ≥30, severe obesity is ≥40. However, BMI has limitations and body composition
matters.

Pathophysiology: Results from chronic energy imbalance (energy intake exceeds expenditure). Involves complex interactions of
genetic, environmental, behavioral, physiological, social, and cultural factors. Adipose tissue dysfunction, altered appetite
regulation (leptin resistance), inflammatory state, and metabolic changes occur.

Health Consequences: Type 2 diabetes, cardiovascular disease, hypertension, dyslipidemia, stroke, certain cancers (breast, colon,
endometrial, kidney), osteoarthritis, sleep apnea, fatty liver disease, GERD, gallbladder disease, reproductive problems,
mental health issues (depression, low self-esteem), and reduced quality of life.

Causes: Overconsumption of calorie-dense foods, physical inactivity, genetic predisposition, certain medications (antidepressants,
antipsychotics, corticosteroids, antidiabetics), medical conditions (hypothyroidism, Cushing's syndrome, PCOS), psychological
factors, insufficient sleep, stress, and socioeconomic factors.

Diagnosis: BMI calculation, waist circumference measurement (central obesity indicator), body composition analysis, assessment
of complications, and evaluation for secondary causes.

Treatment: Multifaceted approach. Lifestyle modifications: dietary changes (caloric restriction, balanced nutrition, portion
control, behavioral strategies), increased physical activity (150-300 min/week moderate intensity), behavioral therapy, sleep
optimization, stress management. Pharmacotherapy for BMI ≥30 or ≥27 with comorbidities: GLP-1 agonists (semaglutide, liraglutide),
combination medications (phentermine/topiramate, naltrexone/bupropion), orlistat. Bariatric surgery for BMI ≥40 or ≥35 with
comorbidities: gastric bypass, sleeve gastrectomy, adjustable gastric banding. Endoscopic procedures. Long-term maintenance
crucial as obesity is chronic disease requiring ongoing management. Multidisciplinary team approach (physician, dietitian,
exercise specialist, behavioral therapist) most effective.
"""
    },

    # ==========================================
    # PHARMACOLOGY & DRUG CLASSES
    # ==========================================
    {
        "title": "Antibiotics - Mechanism of Action",
        "category": "pharmacology",
        "content": """
Antibiotics are medications that fight bacterial infections by killing bacteria or preventing their growth. They work through
various mechanisms targeting bacterial structures or processes not found in human cells, providing selective toxicity.

Major Classes and Mechanisms:

Beta-Lactams (Penicillins, Cephalosporins, Carbapenems): Inhibit bacterial cell wall synthesis by binding to penicillin-binding
proteins (PBPs), preventing peptidoglycan cross-linking. Bactericidal. Spectrum varies by subclass. Resistance via beta-lactamases
(enzymes that break down beta-lactam ring), altered PBPs, or decreased permeability.

Macrolides (Azithromycin, Clarithromycin, Erythromycin): Bind to 50S ribosomal subunit, inhibiting protein synthesis by blocking
translocation. Bacteriostatic (bactericidal at high concentrations). Good tissue penetration. Resistance via ribosomal modification,
efflux pumps, or enzymatic inactivation.

Fluoroquinolones (Ciprofloxacin, Levofloxacin, Moxifloxacin): Inhibit bacterial DNA gyrase and topoisomerase IV, preventing DNA
replication and repair. Bactericidal. Broad spectrum. Resistance via target mutations, efflux pumps, or plasmid-mediated quinolone
resistance.

Tetracyclines (Doxycycline, Minocycline, Tetracycline): Bind to 30S ribosomal subunit, preventing aminoacyl-tRNA binding.
Bacteriostatic. Broad spectrum including atypical organisms. Resistance via efflux pumps, ribosomal protection proteins.

Aminoglycosides (Gentamicin, Tobramycin, Amikacin): Bind to 30S ribosomal subunit, causing misreading of mRNA and preventing
protein synthesis. Bactericidal. Effective against Gram-negative bacteria. Synergistic with beta-lactams. Nephrotoxic and ototoxic.

Sulfonamides and Trimethoprim: Inhibit folate synthesis pathway. Sulfonamides inhibit dihydropteroate synthase; trimethoprim
inhibits dihydrofolate reductase. Often combined (co-trimoxazole/Bactrim). Bacteriostatic.

Glycopeptides (Vancomycin, Teicoplanin): Inhibit cell wall synthesis by binding to D-alanyl-D-alanine terminus of peptidoglycan
precursors. Bactericidal. Active against Gram-positive bacteria including MRSA.

Important Concepts: Bactericidal vs bacteriostatic, spectrum of activity, resistance mechanisms (enzymatic inactivation, target
modification, decreased permeability, efflux pumps), pharmacokinetics (absorption, distribution, metabolism, excretion), and
adverse effects varying by class. Antibiotic stewardship critical to prevent resistance.
"""
    },
    {
        "title": "NSAIDs - Anti-Inflammatory Drugs",
        "category": "pharmacology",
        "content": """
Nonsteroidal Anti-Inflammatory Drugs (NSAIDs) are medications with analgesic, antipyretic, and anti-inflammatory properties.
They're among the most commonly used medications worldwide for treating pain, fever, and inflammation.

Mechanism of Action: NSAIDs inhibit cyclooxygenase (COX) enzymes, which convert arachidonic acid to prostaglandins and
thromboxanes. COX-1 is constitutively expressed and involved in homeostatic functions (gastric mucosa protection, platelet
aggregation, renal blood flow). COX-2 is inducible during inflammation.

Types: Non-selective COX inhibitors (inhibit both COX-1 and COX-2) - aspirin, ibuprofen, naproxen, indomethacin, ketorolac,
diclofenac. Selective COX-2 inhibitors (coxibs) - celecoxib, etoricoxib. Aspirin irreversibly inhibits COX; others are reversible.

Pharmacological Effects: Analgesia (pain relief through reduced prostaglandin synthesis in peripheral tissues and CNS),
antipyretic (fever reduction by inhibiting prostaglandin E2 in hypothalamus), anti-inflammatory (decreased prostaglandin-mediated
inflammation), and antiplatelet (aspirin specifically - irreversible COX-1 inhibition in platelets prevents thromboxane A2
production).

Clinical Uses: Mild to moderate pain (headache, dental pain, musculoskeletal pain), fever, inflammatory conditions (rheumatoid
arthritis, osteoarthritis, ankylosing spondylitis), acute gout, dysmenorrhea, and cardiovascular prophylaxis (low-dose aspirin).

Adverse Effects: Gastrointestinal (most common - dyspepsia, ulcers, bleeding, perforation due to reduced gastroprotective
prostaglandins), cardiovascular (hypertension, increased risk of MI and stroke especially with COX-2 inhibitors and chronic
high-dose use), renal (acute kidney injury, electrolyte disturbances, reduced renal blood flow), hypersensitivity reactions
(aspirin-exacerbated respiratory disease, urticaria), hepatotoxicity (rare), and bleeding risk (especially aspirin).

Contraindications: Active peptic ulcer disease, severe renal impairment, severe heart failure, aspirin/NSAID allergy, third
trimester pregnancy, and post-CABG surgery (COX-2 inhibitors).

Drug Interactions: Anticoagulants (increased bleeding risk), other NSAIDs (increased GI toxicity), corticosteroids (increased
GI bleeding risk), ACE inhibitors and diuretics (reduced efficacy, increased renal toxicity), and methotrexate (increased
toxicity).

Risk Reduction: Use lowest effective dose for shortest duration, take with food, consider proton pump inhibitor for GI protection
in high-risk patients, monitor renal function and blood pressure, avoid in patients with cardiovascular risk if possible.
"""
    }
]


def get_knowledge_by_category(category):
    """Get all knowledge entries for a specific category"""
    return [item for item in MEDICAL_KNOWLEDGE if item['category'] == category]


def get_all_categories():
    """Get list of all unique categories"""
    return list(set(item['category'] for item in MEDICAL_KNOWLEDGE))


def search_knowledge(query):
    """Simple keyword search across all knowledge (fallback for testing)"""
    query_lower = query.lower()
    results = []

    for item in MEDICAL_KNOWLEDGE:
        title_match = query_lower in item['title'].lower()
        content_match = query_lower in item['content'].lower()

        if title_match or content_match:
            results.append(item)

    return results


# Summary statistics
print(f"Medical Knowledge Base Statistics:")
print(f"Total topics: {len(MEDICAL_KNOWLEDGE)}")
print(f"Categories: {', '.join(sorted(get_all_categories()))}")
print(f"Average content length: {sum(len(item['content']) for item in MEDICAL_KNOWLEDGE) // len(MEDICAL_KNOWLEDGE)} characters")
