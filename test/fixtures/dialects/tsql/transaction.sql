BEGIN TRANSACTION;  
DELETE FROM HumanResources.JobCandidate  
    WHERE JobCandidateID = 13;  
COMMIT;  

BEGIN TRAN;
DELETE FROM HumanResources.JobCandidate
  WHERE JobCandidateID = 13;
ROLLBACK TRAN;

BEGIN TRAN;
SAVE TRANSACTION;
