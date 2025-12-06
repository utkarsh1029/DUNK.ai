import { useState } from 'react';
import BaseChatLayout from './BaseChatLayout';
import { featurePrompts } from '../../utils/featurePrompts';
import { API_BASE_URL } from '../../config/api';

const currency = (value) =>
  new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(value);

const normalizeAmount = (value, unit) => {
  if (!value) return undefined;
  const amount = Number(value.replace(/,/g, ''));
  if (Number.isNaN(amount)) return undefined;
  if (!unit) return amount;

  const unitLower = unit.toLowerCase();
  if (['l', 'lac', 'lakh', 'lakhs'].includes(unitLower)) {
    return amount * 100000;
  }
  if (['cr', 'crore', 'crores'].includes(unitLower)) {
    return amount * 10000000;
  }
  return amount;
};

const cleanNumber = (value) => normalizeAmount(value, null);

const extractNumber = (input, keywords) => {
  for (const keyword of keywords) {
    const regex = new RegExp(
      `${keyword}\\D*(₹|rs\\.?|rupees)?\\s*([\\d,.]+)(?:\\s*(l|lac|lakh|lakhs|cr|crore|crores))?`,
      'i'
    );
    const match = input.match(regex);
    if (match) return normalizeAmount(match[2], match[3]);
  }
  return undefined;
};

const extractYears = (input) => {
  const match = input.match(/(\d+)\s*(years|yrs|year|y)/i);
  return match ? Number(match[1]) : undefined;
};

const extractRate = (input) => {
  const match = input.match(/(\d+(?:\.\d+)?)\s*%/);
  return match ? Number(match[1]) : undefined;
};

const extractPaymentsMade = (input) => {
  const match = input.match(/(\d+)\s*(payments|months|installments)/i);
  return match ? Number(match[1]) : undefined;
};

const extractFrequency = (input) => {
  if (/quarter/i.test(input)) return 'quarterly';
  if (/annual|yearly/i.test(input)) return 'annually';
  return 'monthly';
};

const detectInterestMethod = (input) =>
  /flat/.test(input.toLowerCase()) ? 'flat' : 'reducing';

const STORAGE_KEY = 'loan-clarity-profile';

const DEFAULT_PROFILE = {
  principal: undefined,
  annual_rate: undefined,
  tenure_years: undefined,
  repayment_frequency: 'monthly',
  interest_method: 'reducing',
  payments_made: undefined,
  prepayment_amount: undefined,
  reduce_emi: true,
  monthly_income: undefined,
  existing_emis: undefined,
  desired_loan_amount: undefined,
  emi_to_income_ratio: 0.4,
  processing_fee: undefined,
  other_charges: undefined,
  tax_slab: 30,
  is_first_time_buyer: false,
  is_self_occupied: true,
  loan_type: 'home_loan'
};

const hydrateProfile = (rawProfile = {}) => {
  const hydrated = { ...DEFAULT_PROFILE };
  Object.entries(rawProfile).forEach(([key, value]) => {
    if (value === '' || value === null || value === undefined) {
      return;
    }
    if (typeof value === 'string') {
      const numericValue = Number(value);
      hydrated[key] = Number.isNaN(numericValue) ? value : numericValue;
    } else {
      hydrated[key] = value;
    }
  });
  return hydrated;
};

const REQUIRED_FIELDS = {
  emi: ['principal', 'annual_rate', 'tenure_years'],
  schedule: ['principal', 'annual_rate', 'tenure_years'],
  outstanding: ['principal', 'annual_rate', 'tenure_years', 'payments_made'],
  prepayment: [
    'principal',
    'annual_rate',
    'tenure_years',
    'payments_made',
    'prepayment_amount'
  ],
  settlement: ['principal', 'annual_rate', 'tenure_years', 'payments_made'],
  modify_emi: ['principal', 'annual_rate', 'tenure_years', 'new_emi'],
  modify_tenure: ['principal', 'annual_rate', 'tenure_years', 'new_tenure_years'],
  compare: ['loan_options'],
  tax: ['principal', 'annual_rate', 'tenure_years'],
  eligibility: ['monthly_income', 'annual_rate', 'tenure_years'],
  affordability: [
    'desired_loan_amount',
    'monthly_income',
    'annual_rate',
    'tenure_years'
  ],
  effective_rate: ['principal', 'annual_rate', 'tenure_years'],
  default: ['principal', 'annual_rate', 'tenure_years']
};

const LoanClarityEngineChat = ({ sidebarOpen, setSidebarOpen, user }) => {
  const category = {
    id: 'loan-clarity-engine',
    title: 'Loan Clarity Engine',
    description: 'Calculate and understand loan affordability'
  };

  const prompts = featurePrompts['loan-clarity-engine'];

  const formatEligibility = (data) => {
    return `Loan eligibility summary:\n• Monthly income: ${currency(data.monthly_income)}\n• Maximum EMI capacity: ${currency(
      data.maximum_emi
    )}\n• Available EMI after obligations: ${currency(
      data.available_emi
    )}\n• Maximum loan amount: ${currency(
      data.maximum_loan_amount
    )}\n• Recommended loan amount (80% safety): ${currency(
      data.recommended_loan_amount
    )}\n• Debt-to-income ratio: ${data.debt_to_income_ratio}%\n\nKeep your EMI within ${currency(
      data.available_emi
    )} for a healthy profile.`;
  };

  const formatAffordability = (data) => {
    return `Affordability check for ${currency(
      data.desired_loan_amount
    )}:\n• Required EMI: ${currency(data.required_emi)}\n• Total EMI with existing loans: ${currency(
      data.total_emi_with_existing
    )}\n• Maximum safe EMI: ${currency(
      data.maximum_emi_capacity
    )}\n• Affordable loan amount: ${currency(
      data.affordable_loan_amount
    )}\n• Result: ${data.is_affordable ? '✅ Within limit' : '⚠️ Exceeds safe range'}${
      !data.is_affordable
        ? `\nShortfall vs eligibility: ${currency(Math.abs(data.shortfall))}`
        : ''
    }\n\nActual debt ratio: ${data.emi_to_income_ratio_actual}%`;
  };

  const formatEmi = (payload, data) => {
    return `Reducing balance EMI for ${currency(payload.principal)} @ ${
      payload.annual_rate
    }% for ${payload.tenure_years} years (${payload.repayment_frequency}):\n• EMI: ${currency(
      data.emi
    )}\n• Total interest: ${currency(data.total_interest)}\n• Total payment: ${currency(
      data.total_payment
    )}\n• Payments: ${data.number_of_payments}`;
  };

  const formatComparison = (data) => {
    const summary = data.comparisons
      .map(
        (loan) =>
          `• ${loan.loan_name || 'Option'}: EMI ${currency(
            loan.emi
          )}, total interest ${currency(loan.total_interest)}`
      )
      .join('\n');
    const best = data.best_option;
    return `Loan comparison:\n${summary}\n\nBest option → ${best.loan_name || `Option ${best.index + 1}`} (${currency(
      best.emi
    )}/month, total cost ${currency(best.total_payment)})`;
  };

  const fetchJson = async (url, options) => {
    const response = await fetch(url, options);
    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      throw new Error(body.detail ?? 'Backend request failed.');
    }
    return response.json();
  };

  const baseLoanParams = (userInput, overrides = {}) => {
    const principal =
      extractNumber(userInput, ['principal', 'loan', 'amount']) ||
      overrides.principal ||
      3000000;
    const annualRate =
      extractRate(userInput) || overrides.annual_rate || 9.5;
    const tenureYears =
      extractYears(userInput) || overrides.tenure_years || 20;
    const repaymentFrequency = extractFrequency(userInput);
    const interestMethod = detectInterestMethod(userInput);

    return {
      principal,
      annual_rate: annualRate,
      tenure_years: tenureYears,
      repayment_frequency: repaymentFrequency,
      interest_method: interestMethod,
      ...overrides
    };
  };

  const formatScheduleSummary = (data) =>
    `Generated amortization schedule with ${
      data.schedule.length
    } payments.\nFirst payment: Principal ₹${
      data.schedule[0].principal_paid
    }, Interest ₹${data.schedule[0].interest_paid}\nLast payment: Principal ₹${
      data.schedule[data.schedule.length - 1].principal_paid
    }, Interest ₹${data.schedule[data.schedule.length - 1].interest_paid}\nTotal payments: ${
      data.yearly_summary.length
    } years summarized.`;

  const formatPrepayment = (result) =>
    `Prepayment impact:\n• Original EMI: ${currency(result.original_emi)}\n• Outstanding principal before prepayment: ${currency(
      result.outstanding_principal
    )}\n• New principal: ${currency(result.new_principal)}\n${
      result.new_emi
        ? `• New EMI: ${currency(result.new_emi)}`
        : `• New tenure: ${result.new_tenure_years?.toFixed(2)} years`
    }\n• Interest saved: ${currency(result.interest_saved)}`;

  const formatSettlement = (result) =>
    `Early settlement summary:\n• Outstanding principal: ${currency(
      result.outstanding_principal
    )}\n• Settlement amount: ${currency(result.settlement_amount)}\n• Interest saved: ${currency(
      result.interest_saved
    )}`;

  const formatModifyEmi = (result) =>
    `EMI Modification result:\n• Original EMI: ${currency(result.original_emi)}\n• New tenure: ${result.new_tenure_years?.toFixed(
      2
    )} years\n• Interest saved: ${currency(result.interest_saved)}`;

  const formatModifyTenure = (result) =>
    `Tenure modification result:\n• Original EMI: ${currency(result.original_emi)}\n• New EMI: ${currency(
      result.new_emi
    )}\n• Interest difference: ${currency(result.interest_difference || 0)}`;

  const formatEffectiveRate = (data) =>
    `Effective rate: ${data.effective_rate.toFixed(2)}%\nAPR details:\n• Effective rate: ${data.apr_details.effective_rate.toFixed(
      2
    )}%\n• APR: ${data.apr_details.apr.toFixed(2)}%`;

  const [loanProfile, setLoanProfile] = useState(() => {
    if (typeof window === 'undefined') {
      return { ...DEFAULT_PROFILE };
    }
    const stored =
      window.localStorage.getItem(STORAGE_KEY) ||
      window.localStorage.getItem('loan-clarity-data');
    if (!stored) {
      return { ...DEFAULT_PROFILE };
    }
    try {
      return hydrateProfile(JSON.parse(stored));
    } catch (error) {
      // Silently fail and return default profile if parsing fails
      return { ...DEFAULT_PROFILE };
    }
  });

  const rememberProfile = (updates) => {
    setLoanProfile((prev) => {
      const next = hydrateProfile({ ...prev, ...updates });
      try {
        if (typeof window !== 'undefined') {
          window.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
        }
      } catch (error) {
        console.warn('Failed to persist loan profile', error);
      }
      return next;
    });
  };

  const [pendingIntent, setPendingIntent] = useState(null);
  const [pendingPayload, setPendingPayload] = useState({});

  const generateResponse = async (userInput) => {
    const lowerInput = userInput.toLowerCase();
    const hasWord = (...words) => words.some((w) => lowerInput.includes(w));
    const intent =
      pendingIntent ||
      (hasWord('prepayment', 'pre-pay') && 'prepayment') ||
      (hasWord('early settlement', 'foreclose') && 'settlement') ||
      (hasWord('modify tenure', 'change tenure') && 'modify_tenure') ||
      (hasWord('modify emi', 'change emi') && 'modify_emi') ||
      (hasWord('compare') && 'compare') ||
      (hasWord('tax') && 'tax') ||
      (hasWord('eligibility') && 'eligibility') ||
      (hasWord('afford', 'can i afford') && 'affordability') ||
      (hasWord('effective rate', 'apr') && 'effective_rate') ||
      (hasWord('schedule', 'amortization') && 'schedule') ||
      (hasWord('outstanding', 'balance') && 'outstanding') ||
      'emi';

    const fields = new Set(REQUIRED_FIELDS[intent] || REQUIRED_FIELDS.default);
    const basePayload =
      pendingPayload.intent === intent
        ? pendingPayload.data
        : { ...loanProfile };
    const payload = { ...basePayload };

    if (fields.has('principal')) {
      const value = extractNumber(userInput, ['principal', 'loan', 'amount']);
      if (value) payload.principal = value;
    }
    if (fields.has('annual_rate')) {
      const value = extractRate(userInput);
      if (value) payload.annual_rate = value;
    }
    if (fields.has('tenure_years')) {
      const value = extractYears(userInput);
      if (value) payload.tenure_years = value;
    }
    if (fields.has('payments_made')) {
      const value = extractPaymentsMade(userInput);
      if (value) payload.payments_made = value;
    }
    if (fields.has('prepayment_amount')) {
      const value = extractNumber(userInput, ['prepayment', 'lump sum']);
      if (value) payload.prepayment_amount = value;
    }
    if (fields.has('new_emi')) {
      const value = extractNumber(userInput, ['new emi']);
      if (value) payload.new_emi = value;
    }
    if (fields.has('new_tenure_years')) {
      const value = extractYears(userInput);
      if (value) payload.new_tenure_years = value;
    }
    if (fields.has('monthly_income')) {
      const value = extractNumber(userInput, ['income', 'salary']);
      if (value) payload.monthly_income = value;
    }
    if (fields.has('existing_emis')) {
      const value = extractNumber(userInput, ['existing emi']);
      if (value) payload.existing_emis = value;
    }
    if (fields.has('desired_loan_amount')) {
      const value = extractNumber(userInput, ['desired loan', 'loan amount']);
      if (value) payload.desired_loan_amount = value;
    }
    if (fields.has('processing_fee')) {
      const value = extractNumber(userInput, ['processing fee']);
      if (value) payload.processing_fee = value;
    }
    if (fields.has('other_charges')) {
      const value = extractNumber(userInput, ['other charges', 'charges']);
      if (value) payload.other_charges = value;
    }

    const missingFields = [...fields].filter((field) => payload[field] === undefined);
    if (missingFields.length > 0) {
      setPendingIntent(intent);
      setPendingPayload({ intent, data: payload });
      return `I need more info to proceed for ${intent.replace(
        '_',
        ' '
      )}. Please provide: ${missingFields
        .map((field) => field.replace(/_/g, ' '))
        .join(', ')}.`;
    }

    const rememberedFields = [...fields].reduce((acc, field) => {
      if (field === 'loan_options') {
        return acc;
      }
      if (payload[field] !== undefined) {
        acc[field] = payload[field];
      }
      return acc;
    }, {});
    if (Object.keys(rememberedFields).length > 0) {
      rememberProfile(rememberedFields);
    }

    setPendingIntent(null);
    setPendingPayload({});

    if (intent === 'schedule') {
      const schedulePayload = baseLoanParams(userInput, payload);
      schedulePayload.start_date = null;
      const data = await fetchJson(`${API_BASE_URL}/api/loans/schedule`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(schedulePayload)
      });
      return formatScheduleSummary(data);
    }

    if (intent === 'outstanding') {
      const outstandingPayload = baseLoanParams(userInput, payload);
      const data = await fetchJson(
        `${API_BASE_URL}/api/loans/schedule/outstanding`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(outstandingPayload)
        }
      );
      return `Outstanding principal after ${
        outstandingPayload.payments_made
      } payments: ${currency(data.outstanding_principal)}`;
    }

    if (intent === 'prepayment') {
      const prepaymentPayload = baseLoanParams(userInput, payload);
      prepaymentPayload.reduce_emi =
        prepaymentPayload.reduce_emi ??
        (lowerInput.includes('tenure')
          ? false
          : !lowerInput.includes('emi increase'));
      const data = await fetchJson(`${API_BASE_URL}/api/loans/prepayment`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(prepaymentPayload)
      });
      return formatPrepayment(data);
    }

    if (intent === 'settlement') {
      const settlementPayload = baseLoanParams(userInput, payload);
      const data = await fetchJson(
        `${API_BASE_URL}/api/loans/early-settlement`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(settlementPayload)
        }
      );
      return formatSettlement(data);
    }

    if (intent === 'modify_emi') {
      const modifyEmiPayload = baseLoanParams(userInput, payload);
      const data = await fetchJson(`${API_BASE_URL}/api/loans/modify/emi`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(modifyEmiPayload)
      });
      return formatModifyEmi(data);
    }

    if (intent === 'modify_tenure') {
      const modifyTenurePayload = baseLoanParams(userInput, payload);
      const data = await fetchJson(
        `${API_BASE_URL}/api/loans/modify/tenure`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(modifyTenurePayload)
        }
      );
      return formatModifyTenure(data);
    }

    if (intent === 'eligibility') {
      const payload = {
        monthly_income: payload.monthly_income,
        annual_rate: payload.annual_rate,
        tenure_years: payload.tenure_years,
        repayment_frequency: 'monthly',
        interest_method: 'reducing',
        existing_emis: payload.existing_emis ?? 0,
        emi_to_income_ratio: payload.emi_to_income_ratio ?? 0.4
      };
      const data = await fetchJson(`${API_BASE_URL}/api/loans/eligibility`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      return formatEligibility(data);
    }

    if (intent === 'affordability') {
      const payloadData = {
        desired_loan_amount: payload.desired_loan_amount,
        monthly_income: payload.monthly_income,
        annual_rate: payload.annual_rate,
        tenure_years: payload.tenure_years,
        repayment_frequency: 'monthly',
        interest_method: 'reducing',
        existing_emis: payload.existing_emis ?? 0,
        emi_to_income_ratio: payload.emi_to_income_ratio ?? 0.4
      };
      const data = await fetchJson(`${API_BASE_URL}/api/loans/affordability`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payloadData)
      });
      return formatAffordability(data);
    }

    if (lowerInput.includes('compare')) {
      const requestBody = {
        loan_options: [
          {
            principal: extractNumber(userInput, ['₹', 'loan']) || 3000000,
            annual_rate: 9.2,
            tenure_years: 15,
            repayment_frequency: 'monthly',
            interest_method: 'reducing',
            processing_fee: 10000,
            loan_name: 'Bank A (15Y)'
          },
          {
            principal: extractNumber(userInput, ['₹', 'loan']) || 3000000,
            annual_rate: 8.9,
            tenure_years: 20,
            repayment_frequency: 'monthly',
            interest_method: 'reducing',
            processing_fee: 15000,
            loan_name: 'Bank B (20Y)'
          }
        ]
      };
      const data = await fetchJson(`${API_BASE_URL}/api/loans/compare`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestBody)
      });
      return formatComparison(data);
    }

    if (intent === 'effective_rate') {
      const effectiveRatePayload = baseLoanParams(userInput, payload);
      const data = await fetchJson(
        `${API_BASE_URL}/api/loans/effective-rate`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(effectiveRatePayload)
        }
      );
      return formatEffectiveRate(data);
    }

    if (intent === 'tax') {
      const taxPayload = baseLoanParams(userInput, payload);
      taxPayload.loan_type = lowerInput.includes('vehicle')
        ? 'vehicle_loan'
        : lowerInput.includes('personal')
          ? 'personal_loan'
          : 'home_loan';
      taxPayload.tax_slab =
        payload.tax_slab || extractNumber(userInput, ['slab', 'tax']) || 30;
      taxPayload.is_first_time_buyer = lowerInput.includes('first');
      taxPayload.is_self_occupied = !lowerInput.includes('rented');
      const data = await fetchJson(`${API_BASE_URL}/api/loans/tax-benefits`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(taxPayload)
      });
      const annual = data.annual;
      const lifetime = data.lifetime;
      return `Annual tax savings:\n• Section 24: ${currency(
        annual.section_24_deduction
      )}\n• Section 80C: ${currency(annual.section_80c_deduction)}\n• Total tax savings: ${currency(
        annual.tax_savings
      )}\n\nLifetime impact over ${payload.tenure_years} years:\n• Total interest: ${currency(
        lifetime.total_interest
      )}\n• Lifetime savings: ${currency(
        lifetime.lifetime_tax_savings
      )}\n• Net interest after tax: ${currency(lifetime.net_interest_after_tax)}`;
    }

    const emiPayload = baseLoanParams(userInput, payload);

    const data = await fetchJson(`${API_BASE_URL}/api/loans/emi/reducing`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(emiPayload)
    });

    return formatEmi(emiPayload, data);
  };

  return (
    <BaseChatLayout
      category={category}
      prompts={prompts}
      generateResponse={generateResponse}
      sidebarOpen={sidebarOpen}
      setSidebarOpen={setSidebarOpen}
      user={user}
    />
  );
};

export default LoanClarityEngineChat;

