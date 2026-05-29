import ChatPageLayout from './ChatPageLayout';
import LoanClarityEngineChat from '../components/chat/LoanClarityEngineChat';

const category = {
  id: 'loan-clarity-engine',
  title: 'Loan Clarity Engine',
  description: 'Calculate and understand loan affordability'
};

const LoanClarityEnginePage = () => (
  <ChatPageLayout category={category}>
    {(props) => <LoanClarityEngineChat {...props} />}
  </ChatPageLayout>
);

export default LoanClarityEnginePage;

