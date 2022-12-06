(deffunction ask-question (?question $?allowed-values)
   (printout t ?question)
   (bind ?answer (read))
   (if (lexemep ?answer) 
       then (bind ?answer (lowcase ?answer)))
   (while (not (member ?answer ?allowed-values)) do
      (printout t ?question)
      (bind ?answer (read))
      (if (lexemep ?answer) 
          then (bind ?answer (lowcase ?answer))))
   ?answer)

(deffunction yes-or-no-p (?question)
   (bind ?response (ask-question ?question yes no y n))
   (if (or (eq ?response yes) (eq ?response y))
       then yes 
       else no))


(defrule system-banner ""
  (declare (salience 10))
  =>
  (printout t crlf crlf)
  (printout t "The Doctor Suggestion Expert System")
  (printout t crlf crlf))

(defrule print-answer ""
  (declare (salience 10))
  (doctor ?item)
  =>
  (printout t crlf crlf)
  (printout t "Suggested Doctor:")
  (printout t crlf crlf)
  (format t " %s%n%n%n" ?item))
  
;;;***************
;;;* QUERY RULES *
;;;***************

(defrule determine-patient-state ""
   (not (first-aid ?))
   (not (doctor ?))
   =>
   (assert (first-aid (yes-or-no-p "Do you need first-aid (yes/no)? "))))

(defrule determine-sex""
   (first-aid no)
   (not (doctor ?))
   =>
   (assert (sex
      (ask-question "What is your sex (male/female)? "
                    male female))))
              
(defrule determine-injury ""
   (first-aid no)
   (not (doctor ?))
   =>
   (assert (injury (yes-or-no-p "Do you have a physical injury (yes/no)? "))))
    
(defrule determine-head-ill ""
   (first-aid no)
   (injury no)
   (not (doctor ?))
   =>
   (assert (head-ill (yes-or-no-p "Do you have a head ill (yes/no)? "))))
   
(defrule determine-genitals ""
   (first-aid no)
   (injury no)
   (not (doctor ?))
   =>
   (assert (genitals (yes-or-no-p "Do you have a problem with genitals (yes/no)? "))))
   
(defrule determine-skin ""
   (genitals no)
   (not (doctor ?))
   =>
   (assert (skin (yes-or-no-p "Do you have a problem with skin (yes/no)? "))))
   
(defrule determine-ears ""
   (skin no)
   (not (doctor ?))
   =>
   (assert (ears (yes-or-no-p "Do you have a problem with ears (yes/no)? "))))
   
(defrule determine-teeth ""
   (ears no)
   (not (doctor ?))
   =>
   (assert (teeth (yes-or-no-p "Do you have a problem with teeth (yes/no)? "))))
   
(defrule determine-eyes ""
   (teeth no)
   (not (doctor ?))
   =>
   (assert (eyes (yes-or-no-p "Do you have a problem with eyes (yes/no)? "))))
   
(defrule determine-heart ""
   (eyes no)
   (not (doctor ?))
   =>
   (assert (heart (yes-or-no-p "Do you have a problem with heart (yes/no)? "))))
   
(defrule determine-birth ""
   (heart no)
   (sex female)
   (not (doctor ?))
   =>
   (assert (birth (yes-or-no-p "Are you pregnant (yes/no)? "))))
   
;;;****************
;;;* DOCTOR RULES *
;;;****************

(defrule normal-patient-state-conclusions ""
   (first-aid yes)
   (not (doctor ?))
   =>
   (assert (doctor "Immediately go to ambulance.")))
  
(defrule injure-conclusions ""
   (injury yes)
   (not (doctor ?))
   =>
   (assert (doctor "Immediately go to surgeon.")))

(defrule head-ill-conclusions ""
   (injury no)
   (head-ill yes)
   (not (doctor ?))
   =>
   (assert (doctor "Go to neuropatologist.")))

(defrule genitals-conclusions-male ""
   (injury no)
   (genitals yes)
   (not (doctor ?))
   (sex male)
   =>
   (assert (doctor "Go to urologist.")))
   
(defrule genitals-conclusions-female ""
   (injury no)
   (genitals yes)
   (not (doctor ?))
   (sex female)
   =>
   (assert (doctor "Go to gynecologist.")))
   
(defrule skin-conclusions""
   (skin yes)
   (not (doctor ?))
   =>
   (assert (doctor "Go to dermatologist.")))
   
(defrule ears-conclusions""
   (ears yes)
   (not (doctor ?))
   =>
   (assert (doctor "Go to otolaryngologist.")))
   
(defrule teeth-conclusions""
   (teeth yes)
   (not (doctor ?))
   =>
   (assert (doctor "Go to dentist.")))
   
(defrule eyes-conclusions""
   (eyes yes)
   (not (doctor ?))
   =>
   (assert (doctor "Go to ophthalmologist.")))
   
(defrule heart-conclusions""
   (heart yes)
   (not (doctor ?))
   =>
   (assert (doctor "Go to cardiologist.")))
   
(defrule pregnant-conclusions""
   (birth yes)
   (not (doctor ?))
   =>
   (assert (doctor "Go to obstetrician.")))