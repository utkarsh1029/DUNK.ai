import ChatPageLayout from './ChatPageLayout';
import EmergencyFundAssistanceChat from '../components/chat/EmergencyFundAssistanceChat';

const EmergencyFundAssistancePage = () => {
  const category = {
    id: 'emergency-fund-assistance',
    title: 'Emergency Fund Assistance',
    description: 'Plan and manage your emergency funds'
  };

  return (
    <ChatPageLayout category={category}>
      {(props) => <EmergencyFundAssistanceChat {...props} />}
    </ChatPageLayout>
  );
};

export default EmergencyFundAssistancePage;

