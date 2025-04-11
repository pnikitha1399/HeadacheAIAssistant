# Collection of medical knowledge about headaches for the RAG system
# This data would ideally come from reliable medical sources

HEADACHE_KNOWLEDGE = [
    """
    Tension Headache:
    Tension headaches are the most common type of headache and are characterized by mild to moderate pain,
    tightness, or pressure around the forehead or back of the head and neck. These headaches typically
    come on slowly and can last from 30 minutes to several days.
    
    Common symptoms include:
    - Dull, aching head pain
    - Tightness or pressure across the forehead or on the sides and back of the head
    - Tenderness on the scalp, neck, and shoulder muscles
    
    Triggers often include:
    - Stress and anxiety
    - Poor posture
    - Eye strain
    - Fatigue
    - Skipping meals
    
    Treatment approaches include:
    - Over-the-counter pain relievers like ibuprofen or acetaminophen
    - Stress management techniques
    - Regular exercise
    - Proper hydration
    - Maintaining regular sleep schedules
    """,
    
    """
    Migraine Headache:
    Migraines are intense, debilitating headaches often accompanied by other symptoms. They usually
    affect one side of the head and can last from 4 to 72 hours if untreated.
    
    Common symptoms include:
    - Moderate to severe throbbing or pulsing pain
    - Sensitivity to light, sounds, and sometimes smells and touch
    - Nausea and vomiting
    - Visual disturbances or aura (flashing lights, blind spots)
    - Dizziness or light-headedness
    
    Triggers often include:
    - Hormonal changes in women
    - Certain foods and food additives
    - Alcohol and caffeine
    - Stress
    - Changes in sleep patterns
    - Weather changes
    
    Treatment approaches include:
    - Pain-relieving medications (over-the-counter or prescription)
    - Preventive medications for frequent migraines
    - Rest in a quiet, dark room
    - Cold compresses
    - Lifestyle changes to avoid triggers
    """,
    
    """
    Cluster Headache:
    Cluster headaches are rare but extremely painful headaches that occur in cyclical patterns or clusters.
    They're often described as the most painful type of headache.
    
    Common symptoms include:
    - Excruciating pain around or behind one eye
    - Pain that comes on rapidly without warning
    - Restlessness during an attack
    - Redness and tearing of the eye on the affected side
    - Runny or stuffy nose on the affected side
    - Swelling around the eye on the affected side
    
    Triggers often include:
    - Alcohol consumption during a cluster period
    - Strong smells
    - High altitudes
    - Bright light
    
    Treatment approaches include:
    - Oxygen therapy
    - Triptans
    - Local anesthetics
    - Preventive medications
    """,
    
    """
    Sinus Headache:
    Sinus headaches result from inflammation in the sinuses, often due to infection or allergies.
    The pain is localized to the sinus areas of the face.
    
    Common symptoms include:
    - Pain, pressure, and fullness in the cheeks, brow, or forehead
    - Worsening pain when bending forward or lying down
    - Nasal discharge, often discolored
    - Fever (in cases of infection)
    - Decreased sense of smell
    
    Treatment approaches include:
    - Antibiotics (for bacterial sinus infections)
    - Decongestants
    - Nasal steroid sprays
    - Antihistamines for allergy-related sinus headaches
    - Pain relievers
    - Nasal irrigation
    """,
    
    """
    Medication Overuse Headache (Rebound Headache):
    These headaches result from overuse of pain medications used to treat headaches, creating a cycle
    of more frequent headaches and increased medication use.
    
    Common symptoms include:
    - Daily or near-daily headaches
    - Pain that improves with pain medication but returns when medication wears off
    - Neck pain and restlessness
    - Nasal congestion and runny nose
    - Difficulty concentrating
    
    Treatment approaches include:
    - Discontinuation of overused medication (under medical supervision)
    - Transitional medications to help break the cycle
    - Preventive headache medications
    - Lifestyle modifications
    """,
    
    """
    Emergency Headache Warning Signs:
    Certain headache symptoms require immediate medical attention as they may indicate serious conditions
    like stroke, meningitis, or brain hemorrhage.
    
    Seek emergency care for headaches with these characteristics:
    - "Thunderclap" headache (sudden, severe pain that reaches maximum intensity within seconds or minutes)
    - Headache with fever, stiff neck, confusion, seizures, double vision, weakness, or numbness
    - Headache after a head injury
    - Headache that worsens despite treatment
    - New-onset headache in individuals older than 50
    - Headache with pain in the temple area in older adults
    - Headache with exertion, coughing, or sexual activity
    - Headache with changes in vision, speech, or behavior
    
    Do not delay seeking medical help if these warning signs are present.
    """,
    
    """
    Preventive Strategies for Chronic Headaches:
    
    Lifestyle modifications that can help prevent recurring headaches:
    - Maintain regular sleep patterns
    - Stay well-hydrated
    - Eat regular, balanced meals
    - Exercise regularly
    - Manage stress through relaxation techniques
    - Limit or avoid known triggers (certain foods, alcohol, etc.)
    - Maintain good posture, especially when using computers
    - Take regular breaks from screen time
    - Consider biofeedback training
    - Keep a headache diary to identify patterns and triggers
    
    When to consult a doctor:
    - If headaches interfere with daily activities
    - If you're taking headache medication more than twice a week
    - If the pattern or symptoms of your headaches change
    - If headaches worsen or don't improve with over-the-counter treatments
    """,
    
    """
    Children and Headaches:
    Headaches in children have some unique considerations and may present differently than in adults.
    
    Common types in children:
    - Migraine (may be shorter in duration with more pronounced stomach upset)
    - Tension headaches
    - Illness-related headaches
    
    Warning signs requiring medical attention:
    - Headaches that wake a child from sleep
    - Early morning vomiting
    - Headaches that worsen with coughing or exercise
    - Changes in personality or school performance
    - Headaches following head trauma
    
    Management approaches:
    - Proper hydration and regular meals
    - Adequate sleep
    - Limited screen time
    - Stress reduction techniques appropriate for children
    - Age-appropriate pain relievers (as recommended by a pediatrician)
    """,
    
    """
    Headaches During Pregnancy:
    Pregnancy can affect headache patterns, with many women experiencing changes in frequency or intensity
    of pre-existing headaches or developing new headache patterns.
    
    Common patterns:
    - Many women with migraines experience improvement during pregnancy, especially in the second and third trimesters
    - Some women experience their first migraine during pregnancy
    - Tension headaches may worsen with pregnancy-related stress and posture changes
    
    Management considerations:
    - Many headache medications are contraindicated during pregnancy
    - Non-pharmacological approaches are preferred when possible
    - Acetaminophen is generally considered the safest pain reliever during pregnancy
    - Always consult with healthcare providers before taking any medication during pregnancy
    
    When to seek immediate care:
    - Severe headache with high blood pressure (could indicate preeclampsia)
    - Headache with visual changes, especially in the third trimester
    - Any headache that feels "the worst ever" during pregnancy
    """,
    
    """
    Headaches and Mental Health:
    There's a strong connection between headaches and mental health conditions, with each potentially
    exacerbating the other.
    
    Common associations:
    - Anxiety can trigger or worsen tension headaches
    - Depression is more common in people with chronic headaches
    - Post-traumatic stress disorder may be linked to migraine development or worsening
    - Stress is a major trigger for most headache types
    
    Integrated management approaches:
    - Cognitive behavioral therapy
    - Mindfulness and relaxation techniques
    - Stress management
    - Treatment of underlying mental health conditions
    - Support groups for chronic pain
    
    When addressing chronic headaches, mental health evaluation and support should be considered
    as part of a comprehensive treatment plan.
    """
]
