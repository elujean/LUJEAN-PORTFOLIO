// ValidationEngine.js
// This file contains all the validation rules for checking healthcare claims
// Each function checks for a specific type of denial risk

const ValidationEngine = {

    checkEligibility: (claim) => {
        // If member is not activew, they can not recieve services
        if (claim.memberstatus !== "active") {
            return {
                category: "Eligibility",
                severity: "high",
                flag: "Member is not active"
                rationale: "Inactive members cannot recieve covered services",
                recommendation: "Verify member eligibility before resubmitting"
            };
            }
            return null;
        },
    };

    checkAuthorization: (claim) => {
        // Define which CPT codes require prior authorization
        const paRequiredCodes = ["97110", "97140", "97530", "99213", "99214"];

        // Check if any of the claims codes need PA
        const needsPA = claim.cptCodes.some(code => paRequiredCodes.includes(code));

        if (needsPa && !claim.priorAuthNumber) {
            // NLP check: search notes for authorization keywords
            const authPattern = /prior auth|authorization|approved/i;
            const notesHaveAuth = authPattern.test(claim.clinicalNotes);

            if (!notesHaveAuth) {
                return {
                    category: 'Authorization',
                    severity: "high",
                    flag: "Prior authorization required but missing",
                    rationale: 'CPT code(s) ${claim.cptCodes.joing(', ')} require PA',
                    recommendation: "Obtain prior authorization before submission",
                };
            }
        }
        return null;
    }

    checkCodingErrors (claim) => {
        // Check for both specific codes
        const hasBothCodes =
        claim.cptCodes.includes("97110") &&
        claim.cptCodes.includes("97140");

        // Check for the required modifier
        const hasModifier59 = claim.modifiers.includes("59");

        // If we have the problematic combination without the fix
        if (hasBothCodes && !hasModifier59) {
            return {
                category: "Coding/Modifier",
                severity: "medium",
                flag: "Missing modifier 59 for multiple procedures",
                rationale: "CPT 97110 and 97140 billed together require modifier 59",
                recommendation: "Add modifier 59 to the second procedure code"
            };
        }
        return null;
    },

    checkNonCovered: (claim) => {
        // Define cosmetic procedure codes (typically not covered)
    }

export default ValidationEngine ;